def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.endswith('\n'):
                f.write(line)
            else:
                f.write(line + '\n')


def read_lines(path):
    """

    :param path: 文件路径
    :return: 文件内容列表，元素是文件每一行字符串
    """
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]


def parse_records(lines):
    def parse_record(line):
        list_line = line.split(',')
        list_line[2] = float(list_line[2])
        return list_line[0], list_line[1], list_line[2]

    records = list(map(parse_record, lines))
    return records


def find_failed(records):
    fail_records = list(filter(lambda x: x[1] == "FAIL", records))
    return fail_records


def summarize(records):
    if not records:
        raise ValueError("记录列表为空，无法统计")
    total = len(records)
    passed = len(list(filter(lambda x: x[1] == "PASS", records)))
    failed = len(list(filter(lambda x: x[1] == "FAIL", records)))
    passed_rate = passed / total * 100
    avg_duration = sum(list(map(lambda x: x[-1], records))) / total
    summarize_dic = {'total': total, 'passed': passed, 'failed': failed, 'pass_rate': float(f"{passed_rate:.1f}"),
                     'avg_duration': round(avg_duration, 1)}
    return summarize_dic


def format_report(summary, failed):
    summary_lines = ["接口测试报告", f"总用例数: {summary['total']}", f"通过: {summary['passed']}",
                     f"失败: {summary['failed']}", f"通过率: {summary['pass_rate']}%",
                     f"平均耗时: {summary['avg_duration']}s"]
    failed_lines = ["失败明细:"]
    case_ids = [line[0] for line in failed]
    case_costs = [line[2] for line in failed]
    for n, (case_id, case_cost) in enumerate(zip(case_ids, case_costs), start=1):
        failed_lines.append(f"{n}. {case_id}({case_cost}s)")
    summary_lines.extend(failed_lines)
    return summary_lines


if __name__ == '__main__':
    lines = ["TC001,PASS,1.2",
             "TC002,PASS,0.8",
             "TC003,FAIL,3.5",
             "TC004,PASS,2.1",
             "TC005,FAIL,5.0",
             "TC006,PASS,1.5",
             "TC007,PASS,0.9",
             "TC008,FAIL,2.8",
             "TC009,PASS,1.1",
             "TC010,PASS,3.2"]

    write_lines("results.txt", lines)
    test_records = read_lines("results.txt")
    test_parse_records = parse_records(test_records)

    test_failed_records = find_failed(test_parse_records)

    test_summarize = summarize(test_parse_records)
    test_format_report = format_report(test_summarize, test_failed_records)

    write_lines("week3_report.txt", test_format_report)
    read_report = read_lines("week3_report.txt")
    print(' --- week3_report.txt 内容 ---')
    for line in read_report:
        print(line)

    # __name__是文件的内置属性，一般调试模块代码的时候用,如果不放，其他地方调用这个模块会把测试代码执行一遍
    # zip长度不一样，会按照最短的那个去处理
    # write_lines、read_lines是IO,其他是纯计算,分开可以降低认知负荷，提高代码可读性
