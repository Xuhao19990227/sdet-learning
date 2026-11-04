# 导师演示 1.3：requests 库 —— 把 1.1 的 curl 翻译成 Python 函数
# 前置：
#   1) 另一个终端先跑起 demo_http_server.py（本脚本打 http://127.0.0.1:8000）
#   2) week1 的 .venv 已安装 requests：.venv\Scripts\python.exe -m pip install requests
# 运行：.venv\Scripts\python.exe demo_requests_basic.py
#
# 八个小节对应今天的 4 个知识点：
#   S0 探活（ConnectionError：连不上→先查服务器/环境）        → KP1
#   S1 GET 与 Response 五件套                                 → KP2
#   S2 params 与 resp.url（URL 拼接观察）                     → KP2
#   S3 POST：json= vs data=（Content-Type 事故点）+ 写后查    → KP3
#   S4 PUT：亲眼看 demo 的「合并语义」（回收 1.2 可议点）     → KP4
#   S5 DELETE 两次：204→404（幂等观察）                       → KP4
#   S6 /report 授权三连：headers= + 循环（参数化雏形）        → KP4
#   S7 timeout：快速失败                                      → KP4
import sys

import requests

BASE = "http://127.0.0.1:8000"
TIMEOUT = 5  # 生产代码里每个请求都要带 timeout：默认是「永远等」，挂死的源头


def show(resp):
    """统一打印 Response 对象最常用的部位——把 curl -v 看到的东西翻译成代码"""
    print(f"  {resp.request.method} {resp.url} → {resp.status_code}")
    print(f"  Content-Type(响应): {resp.headers.get('Content-Type')}")
    print(f"  body: {resp.text}")


# ---- S0 探活：连不上是最常见的事故，单独捕获 ----
print("=== S0 探活 GET /cases ===")
try:
    resp = requests.get(f"{BASE}/cases", timeout=TIMEOUT)
except requests.exceptions.ConnectionError:
    print("连不上服务器：先在另一个终端启动 demo_http_server.py（排查先查最便宜的）")
    sys.exit(1)
show(resp)  # 200，body 是用例列表的 JSON 数组

# ---- S1 Response 五件套：status_code / json() / text / headers / url ----
print("\n=== S1 Response 对象五件套 ===")
cases = resp.json()  # body 是 JSON 就用 json() 拿 Python 对象（list/dict）；不是 JSON 时调它会抛异常
print(f"  status_code: {resp.status_code}（int 类型，断言直接写 == 200）")
print(f"  共 {len(cases)} 条用例:")
for case in cases:
    print(f"    {case['case_id']} | {case['title']} | {case['level']}")

# ---- S2 params：让 requests 替你拼 URL、做编码 ----
print("\n=== S2 params 与 resp.url ===")
resp = requests.get(f"{BASE}/cases", params={"level": "P0", "page": 2}, timeout=TIMEOUT)
print(f"  实际发出的 URL（resp.url）: {resp.url}")  # → /cases?level=P0&page=2
print(f"  状态码: {resp.status_code}")
# 注意：demo 服务器回 404——它是裸 http.server，把整串 path（含 ?level=P0&page=2）
# 当字符串匹配，不解析 query；真实框架（如 FastAPI）会自动解析查询参数。
# 这个 404 不是 requests 的问题，是服务端局限——resp.url 就是证据。

# ---- S3 POST：json= vs data= + 写后查 ----
print("\n=== S3a POST json= 创建 TC090 ===")
payload = {"case_id": "TC090", "title": "requests 演示用例", "level": "P2"}
resp = requests.post(f"{BASE}/cases", json=payload, timeout=TIMEOUT)
show(resp)  # 201 {"created": "TC090"}；json= 自动把 dict 序列化成 JSON 体并加 Content-Type
print(f"  请求里发出的 Content-Type: {resp.request.headers.get('Content-Type')}")

print("=== S3b POST data=（常见事故点）===")
resp = requests.post(f"{BASE}/cases", data=payload, timeout=TIMEOUT)
show(resp)  # 400！data= 发的是表单编码 case_id=TC090&...，服务器 json.loads 解析不了
print(f"  请求里发出的 Content-Type: {resp.request.headers.get('Content-Type')}")

print("=== S3c 写后查：创建到底成没成 ===")
resp = requests.get(f"{BASE}/cases/TC090", timeout=TIMEOUT)
show(resp)  # 200 且有 TC090 → 测试习惯：POST 断言不止看响应，还要看资源状态

# ---- S4 PUT：1.2 说「全量替换」，demo 实际呢？ ----
print("\n=== S4 PUT 只送 level（观察合并 vs 全量替换）===")
resp = requests.put(f"{BASE}/cases/TC002", json={"level": "P0-演示改"}, timeout=TIMEOUT)
show(resp)  # 200 {"updated": "TC002"}
resp = requests.get(f"{BASE}/cases/TC002", timeout=TIMEOUT)
show(resp)  # title 还在！→ demo 的 PUT 是合并（PATCH 语义），与 1.2 资料「全量替换」不一致 = 可议点
# 测试原则：以文档为基准，实测与文档不一致 → 要么 bug 要么改文档，不允许沉默

# ---- S5 DELETE 两次：幂等观察 ----
print("\n=== S5 DELETE TC090 两次 ===")
resp = requests.delete(f"{BASE}/cases/TC090", timeout=TIMEOUT)
print(f"  第一次: {resp.status_code}, body='{resp.text}'")  # 204，无内容，body 是空串
resp = requests.delete(f"{BASE}/cases/TC090", timeout=TIMEOUT)
print(f"  第二次: {resp.status_code}, body={resp.text}")  # 404 {"error": "用例不存在"}
# 幂等 = 状态效果相同（它就是没了），但响应码可以 204→404
# 204 时调 resp.json() 会抛异常（没有 body）——空体看 text，别无脑 json()

# ---- S6 headers=：授权三连（用循环——参数化的雏形）----
print("\n=== S6 /report 授权三连 ===")
auth_variants = [
    ("不带凭证", {}),
    ("错凭证", {"Authorization": "Bearer wrong"}),
    ("对凭证", {"Authorization": "Bearer secret"}),
]
for label, headers in auth_variants:  # 三组数据打同一个请求 = 2.4 @parametrize 要正式化的事
    resp = requests.get(f"{BASE}/report", headers=headers, timeout=TIMEOUT)
    print(f"  {label}: {resp.status_code} | {resp.text}")
# 预期：401（未认证）→ 403（带了但不对——demo 的可议点，标准惯例回 401）→ 200

# ---- S7 timeout：快速失败 ----
print("\n=== S7 timeout：连一个不存在的服务器 ===")
try:
    requests.get("http://192.0.2.1/", timeout=1)  # 192.0.2.x 是 RFC 5737 保留测试网段，正常必不可达
    print("  居然连上了？")
except requests.exceptions.Timeout:
    print("  触发 Timeout：timeout=1 表示最多等 1 秒——快速失败，而不是永远挂着")
except requests.exceptions.ConnectionError:
    print("  触发 ConnectionError：拒绝/不可达也是快速失败——都比默认的无限等待强")

print("\n演示结束。轮到你写：练习/week1/lesson3.py（题目见 lesson3_题目.md）")
