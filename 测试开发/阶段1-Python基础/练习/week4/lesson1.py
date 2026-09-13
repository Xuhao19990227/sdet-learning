class TestCase:

    def __init__(self, case_id, title, priority):
        self.case_id = case_id
        self.title = title
        self.priority = priority

    def is_p0(self):
        return self.priority == 'P0'

    def describe(self):
        return f"{self.case_id} [{self.priority}] {self.title}"


if __name__ == '__main__':

    test_cases = [TestCase("TC001", "登录接口校验", "P0"), TestCase("TC002", "查询订单列表", "P1"),
                  TestCase("TC003", "支付接口金额校验", "P0")]
    for testcase in test_cases:
        print(testcase.describe())
    p0_cases = list(filter(lambda x: x.is_p0(), test_cases))
    print(f"P0 用例数: {len(p0_cases)}")
