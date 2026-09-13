cases = [
    {"name": "登录接口", "expected": 200, "actual": 200},
    {"name": "查询用户", "expected": 200, "actual": 500},
    {"name": "删除用户", "expected": 204, "actual": 204},
    {"name": "越权访问", "expected": 403, "actual": 200},
]
failcases_no = []
for n, case in enumerate(cases, start=1):
    if case["expected"] == case["actual"]:
        print(f"用例{n} {case['name']}: PASS")
    else:
        failcases_no.append(f"#{n}")
        print(f"用例{n} {case['name']}: FAIL (期望 {case['expected']}, 实际 {case['actual']})")

print(f"共{len(cases)}条用例, 失败{len(failcases_no)}条, 编号: {', '.join(failcases_no)}")


# 返回的是迭代器，第二遍什么都没有
# 因为sum是内置函数，会把内置函数覆盖，我会取名为fail_count


# ===== 练习2：zip 数据驱动报告 =====
def data_driven_report(case_names, expected_codes, actual_codes):
    fail_cases_name = []
    if not len(case_names) == len(expected_codes) == len(actual_codes):
        raise ValueError(f"数据列长度不一致: {len(case_names)}/{len(expected_codes)}/{len(actual_codes)}")
    for n, (case_name, expected_code, actual_code) in enumerate(zip(case_names, expected_codes, actual_codes), start=1):
        if expected_code == actual_code:
            print(f"用例{n} {case_name}: PASS")
        else:
            fail_cases_name.append(case_name)
            print(f"用例{n} {case_name}: FAIL (期望 {expected_code}, 实际 {actual_code})")

    print(f"失败接口: {fail_cases_name}")


case_names = ["登录接口", "查询用户", "删除用户", "越权访问"]
expected_codes = [200, 200, 204, 403]
actual_codes = [200, 500, 204, 200]

data_driven_report(case_names, expected_codes, actual_codes)

# zip会用最短的那个列表长度迭代，先判断列表长度是否一致，如果不一致就抛出异常
# 括号去掉会报错，enumerate只会提供两个值，括号去掉就有四个参数去匹配两个值，值不够


# ===== 练习3：map/filter 综合 =====

results = [
    {"case_id": "API-001", "name": "登录接口", "status": "PASS", "cost": 1.2},
    {"case_id": "API-002", "name": "查询用户", "status": "FAIL", "cost": 0.3},
    {"case_id": "API-003", "name": "删除用户", "status": "FAIL", "cost": 2.8},
    {"case_id": "API-004", "name": "越权访问", "status": "PASS", "cost": 0.5},
    {"case_id": "API-005", "name": "导出报表", "status": "PASS", "cost": 3.6},
]

case_ids = list(map(lambda x: x["case_id"], results))
fail_cases = list(filter(lambda x: x["status"] == "FAIL", results))
fail_cases_name = [case["name"] for case in fail_cases]
pass_cases = list(filter(lambda x: x["status"] == "PASS", results))
passed_rate = len(pass_cases) / len(results) * 100
sorted_cases = sorted(results, key=lambda x: x["cost"], reverse=True)
print(f"全部用例ID: {case_ids}")
print(f"失败用例: {fail_cases_name}")
print(f"通过率: {passed_rate:.1f}%")
print(f"最慢用例: {sorted_cases[0]['name']} ({sorted_cases[0]['cost']}s)")

# 看到的是迭代器本身，遍历第二遍会无法遍历，第一遍已经遍历完了
# 数据全换成FAIL，通过率输出0.0%,我的代码不会崩
