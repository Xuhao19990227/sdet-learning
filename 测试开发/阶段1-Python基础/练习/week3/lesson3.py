def is_passed(status):
    """
    判断是否通过，PASS返回True,其他返回False
    :param status:状态字符串 str
    :return:bool
    """
    return status == "PASS"


def get_stats(results):
    """
    传入状态列表返回统计结果
    :param results: 状态list/tuple
    :return: 总数int，通过数int，失败率float
    """
    if not results:
        return 0, 0, 0.0

    total = len(results)
    passed = results.count("PASS")
    fail_rate = (total - passed) / total * 100
    return total, passed, fail_rate


def judge_level(rate):
    """
    传入通过率返回评级
    :param rate: 通过率 int/float
    :return: 评级 str
    """
    if rate >= 95:
        return "优秀"
    if rate >= 80:
        return "良好"
    if rate >= 60:
        return "及格"
    return "不及格"


results = ["PASS", "FAIL", "PASS", "PASS", "SKIP"]

passed_list = [passed for passed in results if is_passed(passed)]
print(f"通过用例数: {len(passed_list)}")

total, passed, fail_rate = get_stats(results)
print(f"共 {total} 条, 通过 {passed} 条, 失败率 {fail_rate:.1f}%")

rate_list = [95, 94.9, 80, 79.9, 60, 59.9]

for rate in rate_list:
    print(f"{rate} → {judge_level(rate)}")
