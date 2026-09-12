path = input("接口地址：")
status_code = int(input("状态码："))
cost = float(input("耗时："))
case_total = int(input("用例总数："))
fail_case_total = int(input("失败数："))

check = status_code == 200 and cost < 1

pass_rate = f"{(case_total - fail_case_total) / case_total:.1%}" if case_total else "0.0%"

estimate = f"{case_total * 1000:,}"

time_consuming = f"{cost:.3f}"

print("=====","测试报告",sep=' ',end=' ')
print("=====")
print("接口地址:",path)
print("状态码:", f"{status_code},","检查通过:",check)
print("用例总数:", case_total, "失败数:", fail_case_total)
print("响应时间: ",time_consuming,"秒",sep='')
print("通过率:",pass_rate)
print("预估请求总数:",estimate)
print("=====================")
