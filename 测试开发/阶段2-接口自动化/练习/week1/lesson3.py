import requests

host = "http://127.0.0.1:8000"

result_T1 = requests.get(host + "/cases", timeout=5)
print(result_T1.status_code)
cases = result_T1.json()
print(len(cases))
for case in cases:
    print(case["case_id"], case["title"], case["level"])

result_T2_01 = requests.get(host + "/cases/TC999", timeout=5)
print(result_T2_01.status_code)
print(result_T2_01.json())

result_T2_02 = requests.get(host + "/nope", timeout=5)
print(result_T2_02.status_code)
print(result_T2_02.json())

result_T3_01 = requests.post(host + "/cases", timeout=5,
                             json={"case_id": "TC004", "title": "支付回调验证", "level": "P1"})

print(result_T3_01.status_code)
print(result_T3_01.json())

result_T3_02 = requests.get(host + "/cases/TC004", timeout=5)

print(result_T3_02.status_code)
print(result_T3_02.json())

headers_T4 = [{}, {"authorization": "Bearer wrong"}, {"authorization": "Bearer secret"}]
for header in headers_T4:
    result_T4 = requests.get(host + "/report", timeout=5, headers=header)
    print(result_T4.status_code)
    print(result_T4.json())

result_T5_01 = requests.put(host + "/cases/TC001", timeout=5, json={"level": "P0-作业"})
print(result_T5_01.status_code)
print(result_T5_01.json())

result_T5_02 = requests.get(host + "/cases/TC001", timeout=5)
print(result_T5_02.status_code)
print(result_T5_02.json())
print("结论: title 仍是'登录接口验证'、只有 level 变了 → demo 的 PUT 是合并语义，与 1.2 资料说的'PUT=全量替换'不一致")

for i in range(2):
    result_T6 = requests.delete(host + "/cases/TC004", timeout=5)
    print(result_T6.status_code)
    print(result_T6.text)

result_T7_01 = requests.post(host + "/cases", json={"case_id": "TC001", "title": "重复创建测试", "level": "P9"},
                             timeout=5)

print(result_T7_01.status_code)
print(result_T7_01.json())

result_T7_02 = requests.get(host + "/cases/TC001", timeout=5)
print(result_T7_02.status_code)
print(result_T7_02.json())

# 1.json= 生成 Content-Type: application/json，body 序列化为 JSON 字符串；
#   data= 生成 Content-Type: application/x-www-form-urlencoded，body 是 a=1&b=2 表单格式。
#   T3 若误用 data=：服务器 json.loads 解析表单编码失败 → 回 400"请求体不是合法 JSON"，
#   TC004 不会落库（导师实测 B2/B3：POST 400，写后查 GET 404）。
# 2.不写 timeout 时 requests 默认永远等待（不会超时），脚本可能挂死。
#   POST 超时后不能自动重试，由【接口是否幂等】决定：POST 不幂等，且超时≠失败——
#   数据可能已插入成功，盲重试=重复写入（可能被防重拦截，也可能造成重复下单）；
#   GET/PUT/DELETE 幂等才可安全自动重试。POST 真要重试需服务端支持幂等键(Idempotency-Key)。
# 3.标题：《PUT接口实际行为与文档不符》
# 结论：put接口实际功能是数据字段修改功能，不是文档描述的全量替换
# 证据：我发了什么请求PUT + /cases/TC001 + {"level": "P0-作业"}→ 文档原话写的是全量替换 → 实测只是修改了字段level为P0-作业，没传的字段没有修改，合并语义（局部更新），实为 PATCH 的职责
# 落点：（应该修改接口功能？需找开发确认是否设计如此）+ 风险（调用方按"全量替换"可能会发生想清掉某个字段的值清不掉）
