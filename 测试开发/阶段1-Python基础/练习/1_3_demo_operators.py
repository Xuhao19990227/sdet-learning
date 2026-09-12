"""
课时 1.3 演示代码：运算符
场景：统计一组接口测试的响应时间，并判断接口是否达标
运行方式：python 1_3_demo_operators.py
"""

# ========== 1. 算术运算符 ==========
# 模拟 3 次接口请求的响应时间（秒）
time_first = 0.523
time_second = 0.487
time_third = 1.010

total_time = time_first + time_second + time_third   # 加法：总耗时
avg_time = total_time / 3                            # 除法：平均耗时（结果永远是 float）
print("总耗时:", total_time)
print("平均耗时:", round(avg_time, 3))               # round() 保留3位小数

# / 与 // 的区别
print("7 / 2 =", 7 / 2)      # 3.5   普通除法，结果是 float
print("7 // 2 =", 7 // 2)    # 3     整除（向下取整）
print("7 % 2 =", 7 % 2)      # 1     取余（模运算）
print("2 ** 10 =", 2 ** 10)  # 1024  幂运算

# 测试场景：把 130 秒换算成 "2分10秒"
seconds = 130
minutes = seconds // 60       # 整除得到分钟数
rest = seconds % 60           # 取余得到剩余秒数
print(f"{seconds}秒 = {minutes}分{rest}秒")


# ========== 2. 比较运算符（结果是 bool） ==========
status_code = 200
response_time = 0.523

print("status_code == 200 :", status_code == 200)   # True  等于
print("status_code != 200 :", status_code != 200)   # False 不等于
print("response_time < 1 :", response_time < 1)     # True  小于

# Python 支持链式比较（很多语言不支持）
score = 85
print("60 <= score < 90 :", 60 <= score < 90)       # True，等价于 60<=score and score<90


# ========== 3. 逻辑运算符 ==========
is_success = (status_code == 200)
is_fast = (response_time < 1)

print("is_success and is_fast :", is_success and is_fast)  # 两个都为True才是True
print("is_success or is_fast  :", is_success or is_fast)   # 有一个True就是True
print("not is_success         :", not is_success)          # 取反

# 测试场景：判断用例是否通过 —— 状态码正确 且 耗时达标 且 没有报错
has_error = False
case_passed = is_success and is_fast and (not has_error)
print("用例是否通过:", case_passed)


# ========== 4. 赋值运算符 ==========
pass_count = 0
pass_count += 1     # 等价于 pass_count = pass_count + 1
print("pass_count:", pass_count)   # 1

fail_count = 10
fail_count -= 3     # 7
fail_count *= 2     # 14
print("fail_count:", fail_count)

total = 20
total //= 3         # 6  整除后赋值
total %= 4          # 2  取余后赋值
print("total:", total)

# 注意：Python 没有 ++ 和 -- ！
count = 5
# count++   # ❌ 语法错误！Python 不支持
count += 1  # ✅ 正确写法
print("count:", count)
