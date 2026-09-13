class TestResult:
    total_count = 0

    def __init__(self, case_id, status, duration):
        if not TestResult.is_valid_status(status):
            raise ValueError(f"非法状态：{status}")
        self.case_id = case_id
        self.status = status
        self.duration = duration
        TestResult.total_count += 1

    def is_failed(self):
        return self.status == 'FAIL'

    def describe(self):
        return f"{self.case_id} [{self.status}] {self.duration}s"

    @staticmethod
    def is_valid_status(status):
        return status in ["PASS", "FAIL"]

    @classmethod
    def from_csv_line(cls, line):
        case_id, case_status, case_duration = line.split(',')
        return cls(case_id, case_status, float(case_duration))

    @classmethod
    def get_total_count(cls):
        return cls.total_count


if __name__ == '__main__':
    lines = ["TC001,PASS,1.2", "TC002,FAIL,3.5", "TC003,PASS,0.8", "TC004,FAIL,5.0", "TC005,PASS,2.1"]

    examples = list(map(TestResult.from_csv_line, lines))
    for result in examples:
        print(result.describe())

    print(f"失败数: {len(list(filter(lambda x: x.is_failed(), examples)))}")
    print(f"总用例数: {TestResult.get_total_count()}")
