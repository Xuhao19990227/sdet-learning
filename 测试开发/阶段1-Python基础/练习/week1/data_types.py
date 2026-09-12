api_name = "用户登录"
status_code = 200
response_time = 0.523
is_success = True

print(type(api_name))
print(type(status_code))
print(type(response_time))
print(type(is_success))

print("[接口测试]",api_name,"-","状态码:"+str(status_code),"-",f"耗时:{response_time}s")