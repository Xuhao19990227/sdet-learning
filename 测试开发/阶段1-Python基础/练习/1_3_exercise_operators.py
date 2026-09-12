"""
课时 1.3 练习题：接口测试结果统计小程序
要求：把 5 个 TODO 补全，使程序输出与「预期输出」完全一致
运行方式：python 1_3_exercise_operators.py
"""

# 已知数据：3 个接口的响应时间（秒）和状态码
time_a, code_a = 0.32, 200
time_b, code_b = 1.25, 200
time_c, code_c = 0.88, 500

# TODO 1: 用算术运算符计算 3 个接口的总耗时 total_time 和平均耗时 avg_time
#         （平均耗时用 round(avg_time, 2) 保留两位小数输出）


# TODO 2: 用比较运算符判断每个接口是否"达标"：
#         达标条件 = 状态码等于 200 且 响应时间小于 1 秒
#         分别得到 ok_a, ok_b, ok_c 三个 bool 值
#         提示：需要用 and 把两个比较结果连起来


# TODO 3: 用赋值运算符统计达标数量 pass_count：
#         初始为 0，每达标一个就 += 1（用 if 判断 ok_x 是否为 True）


# TODO 4: 用整除和取余，把总耗时换算成整秒和毫秒两部分：
#         total_ms = int(round(total_time * 1000))   # 总毫秒数（已给出）
#         total_ms = int(round(total_time * 1000))
#         sec = ...   # total_ms 里包含多少个完整的 1000 毫秒（整除）
#         ms = ...    # 剩下多少毫秒（取余）


# TODO 5: 用逻辑运算符判断整批测试是否通过 all_passed：
#         条件：3 个接口全部达标（提示：用 and 连接 ok_a, ok_b, ok_c）


# ===== 输出区（补全 TODO 后取消注释）=====
# print("总耗时:", total_time)
# print("平均耗时:", round(avg_time, 2))
# print("接口A达标:", ok_a)
# print("接口B达标:", ok_b)
# print("接口C达标:", ok_c)
# print("达标数量:", pass_count)
# print(f"{total_time}秒 = {sec}秒{ms}毫秒")
# print("整批测试是否通过:", all_passed)

"""
预期输出：
总耗时: 2.45
平均耗时: 0.82
接口A达标: True
接口B达标: False
接口C达标: False
达标数量: 1
2.45秒 = 2秒450毫秒
整批测试是否通过: False
"""
