class TestCase:
    """用例类"""

    def __init__(self, case_id, status="NOT_RUN"):
        self.case_id = case_id
        self.status = status

    def __str__(self):
        return f"[{self.case_id}] {self.status}"

    def __repr__(self):
        return f"TestCase({self.case_id!r}, {self.status!r})"

    def __eq__(self, other):
        if not isinstance(other, TestCase):
            return False
        return self.case_id == other.case_id


class CaseSuite:
    """套件类"""

    def __init__(self, name, cases):
        self.name = name
        self.cases = cases

    def __len__(self):
        return len(self.cases)

    def __str__(self):
        return f"套件 {self.name}：{len(self)} 条用例"


if __name__ == '__main__':
    c1 = TestCase("TC001", "PASS")
    c2 = TestCase("TC001", "FAIL")
    c3 = TestCase("TC003", "FAIL")
    suite = CaseSuite("登录模块", [c1, c2, c3])

    print(c1)
    print(repr(c3))
    print([c1, c3])
    print(c1 == c2)
    print(c1 is c2)
    print(c1 == "TC001")
    print(len(suite))
    print(suite)

    # 1.TestCase('TC001', 'PASS')
    # 2.因为他们的实例都指向True,由开发者决定，在断言的时候
    # 3.list的用途一般是聚合报告，__repr__合适
    # 4.TypeError: 'str' object cannot be interpreted as an integer
