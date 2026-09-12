bug_ids = [101, 102, 103, 101, 104, 102, 101]
planned = {"login", "pay", "register", "search", "cart"}
executed = {"login", "pay", "logout", "search"}
case = ("login", 200, 0.35)

bugs = sorted(set(bug_ids))
print(bugs)

for bug in bugs:
    print("bug", bug, "出现", bug_ids.count(bug), "次")

print("漏执行的用例", planned - executed)
print("计划外执行的用例", executed - planned)
print("正常覆盖的用例", planned & executed)

case, code, cost = case
print(f"用例 {case} 状态码 {code} 耗时 {cost}s")

# 因为tuple是不可变的数据类型，list是可变的数据类型，字典的key只能是不可变数据类型


