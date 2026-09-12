def print_separator():
    """
    打印分割线
    :return: None
    """
    print("-" * 30)


def show_case_info(case_id, title, status):
    """
    打印用例执行结果
    :param case_id: 用例id
    :param title: 用例标题
    :param status: 用例结果
    :return: None
    """
    print(f"用例编号: {case_id}")
    print(f"用例标题: {title}")
    print(f"执行状态: {status}")


def show_summary(total, passed):
    """
    打印用例执行统计结果
    :param total: 执行用例数量
    :param passed: 用例通过数量
    :return: None
    """
    print_separator()
    print(f"执行结果: 共 {total} 条, 通过 {passed} 条")
    if total:
        print(f"通过率: {passed / total:.1%}")
    else:
        print("暂无执行用例")


show_case_info('API-001', '登录成功验证', 'PASS')
show_case_info('API-002', '密码错误返回401', 'FAIL')
show_summary(10, 8)
