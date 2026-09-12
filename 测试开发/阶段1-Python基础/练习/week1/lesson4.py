raw_log = "  2026-09-06 22:10:15 [ERROR] /v1/orders/query 响应超时, 耗时3.52秒  "
base_url = "https://mall-api.example.com"
endpoint = "/v1/orders/query"

log = raw_log.strip()
date = log.split(' ')[0]
level = log.split(' ')[2]
is_query = endpoint.endswith('query')
url = base_url + endpoint
is_https = url.startswith("https")
fixed_log = log.replace("ERROR", "WARN")
has_timeout = "超时" in log
cost = 3.52

print("日期:", date)
print("级别:", level)
print("是查询接口:", is_query)
print('完整URL:', url)
print("是否HTTPS:", is_https)
print("修改后:", fixed_log)
print("包含超时:", has_timeout)
print(f"报告: 用例[/v1/orders/query] 失败, 耗时{cost:.1f}秒, 原因: 响应超时")
