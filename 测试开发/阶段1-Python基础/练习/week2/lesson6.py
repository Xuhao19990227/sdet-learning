test_records = [
    ("login", 200, 0.32, True),
    ("get_user", 200, 0.15, True),
    ("create_order", 201, 0.87, True),
    ("login", 500, 2.31, False),
    ("pay", 200, 1.20, True),
    ("get_user", 404, 0.08, False),
    ("create_order", 201, 0.92, True),
    ("pay", 200, 1.05, True),
    ("login", 200, 0.28, True),
    ("refund", 500, 3.10, False),
]

total = len(test_records)
pass_total = len([record for record in test_records if record[-1]])
fail_total = len([record for record in test_records if not record[-1]])

pass_rate = f"{pass_total / total:.1%}"

print(f"总用例：{total}，通过：{pass_total}，失败：{fail_total}，通过率：{pass_rate}")

apis = sorted(list(set([record[0] for record in test_records])))
print(apis)

fail_records = [record for record in test_records if not record[-1]]
for record in fail_records:
    print(f"[FAIL] {record[0]} - {record[1]}")

cost_max_record = max(test_records, key=lambda x: x[2])
acount_api = {}
for record in test_records:
    api = record[0]
    acount_api[api] = acount_api.get(api, 0) + 1
print(acount_api)
print(f"最慢接口：{cost_max_record[0]}（{cost_max_record[2]:.2f}s）")

avg_cost = f"{sum([record[2] for record in test_records]) / total:.2f}"

print(f"平均耗时：{avg_cost}s")
report = {
    "total": total,
    "passed": pass_total,
    "failed": fail_total,
    "pass_rate": pass_rate,
    "avg_cost": float(avg_cost),
    "slowest": cost_max_record[0],
    "failed_apis": list(dict.fromkeys([record[0] for record in fail_records]))
}

print(report)

# 思考题

# from collections import Counter
#
# apis_count = Counter([record[0] for record in test_records]).most_common()
# print(apis_count)
# dic = {}
# for i in apis_count:
#   dic[i[0]] = "i[1]次"
# print(dic)
