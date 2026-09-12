cases = [
    {"case_id": "API-001", "title": "登录成功", "status": "PASS", "cost": 1.2},
    {"case_id": "API-002", "title": "密码错误", "status": "FAIL", "cost": 0.3},
    {"case_id": "API-003", "title": "验证码过期", "status": "FAIL", "cost": 2.8},
    {"case_id": "API-004", "title": "退出登录", "status": "PASS", "cost": 0.9},
    {"case_id": "API-005", "title": "token刷新", "status": "SKIP", "cost": 0.1},
]

s_cases = sorted(cases, key=lambda x: x["cost"], reverse=True)
print(f"最慢用例: {s_cases[0]['case_id']}, 耗时 {s_cases[0]['cost']}s")

cost_max_case = max(cases, key=lambda x: x["cost"])
print(f"耗时最大: {cost_max_case['title']}")
fail_cases = filter(lambda x: x["status"] == "FAIL", cases)
print(f"失败用例: {[case['case_id'] for case in fail_cases]}")

case_overview = list(map(lambda x: f"{x['case_id']}({x['status']})", cases))
print(f"用例概览: {case_overview}")
