class ApiCase:
    """
    运行API测试的类
    """

    def __init__(self, case_id, url):
        self.case_id = case_id
        self.url = url

    def run(self):
        print(f"[API] {self.case_id}: GET {self.url} -> 状态码 200")
        return "PASS"


class UICase:
    """
    运行UI测试的类
    """

    def __init__(self, case_id, element):
        self.case_id = case_id
        self.element = element

    def run(self):
        if not self.element:
            print(f"[UI] {self.case_id}: 元素未找到")
            return "FAIL"
        else:
            print(f"[UI] {self.case_id}: 点击 {self.element}")
            return "PASS"


class Report:
    """
    生成测试报告的类
    """

    def __init__(self):
        self.__records = []

    def add(self, case_id, status):
        self.__records.append((case_id, status))

    def summary(self):
        total_num = len(self.__records)
        passed_num = len([record for record in self.__records if record[1] == "PASS"])
        failed_num = len([record for record in self.__records if record[1] == "FAIL"])
        return f"总数 {total_num}，PASS {passed_num}，FAIL {failed_num}"


def batch_run(cases, report):
    for case in cases:
        case_status = case.run()
        report.add(case.case_id, case_status)


if __name__ == '__main__':
    cases = [
        ApiCase("TC001", "/api/login"),
        UICase("TC002", "#submit"),
        ApiCase("TC003", "/api/logout"),
        UICase("TC004", ""),
    ]
    report = Report()
    batch_run(cases, report)
    print(report.summary())

    # 1.是哪个类的实例就跑哪个的run()
    # 2.AttributeError: 'Report' object has no attribute '__records';[('TC001', 'PASS'), ('TC002', 'PASS'), ('TC003', 'PASS'), ('TC004', 'FAIL')]
    # 3.不需要改动代码，只需要新增一个PerfCase类就可以了，无需修改原有代码，降低引入bug风险
