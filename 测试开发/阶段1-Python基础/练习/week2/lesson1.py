status_code = int(input("状态码："))

if status_code == 200:
    print("200        → ✅ 请求成功")
elif status_code == 301 or status_code == 302:
    print("301 或 302 → ↪ 重定向")
elif status_code == 404:  # 404在400到500之间，需要写在前面，不然会被4xx范围分支先截获
    print("404        → ❌ 资源不存在")
elif 400 <= status_code < 500:
    print("其余 4xx   → ⚠ 客户端错误")
elif 500 <= status_code < 600:
    print("5xx        → 🔥 服务端错误")
else:
    print("其他       → ❓ 未知状态码")
