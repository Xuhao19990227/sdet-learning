time_a, code_a = 0.32, 200
time_b, code_b = 1.25, 200
time_c, code_c = 0.88, 500


total_time = time_a + time_b + time_c

avg_time = total_time / 3

ok_a = code_a == 200 and time_a < 1
ok_b = code_b == 200 and time_b < 1
ok_c = code_c == 200 and time_c < 1


pass_count = sum([ok_a, ok_b,ok_c])

total_ms = int(round(total_time * 1000))
sec = total_ms // 1000
ms = total_ms % 1000
all_passed = ok_a and ok_b and ok_c


print(f"总耗时: {total_time}")
print(f"平均耗时: {round(avg_time,2)}")
print(f"接口A达标: {ok_a}")
print(f"接口B达标: {ok_b}")
print(f"接口C达标: {ok_c}")
print(f"达标数量: {pass_count}")
print(f"{total_time}秒 = {sec}秒{ms}毫秒")
print(f"整批测试是否通过: {all_passed}")

