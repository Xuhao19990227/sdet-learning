"""5.4 课内演示3：生成器管道——日志分析三层流水线（周练习的骨架）
要点：每层都是生成器，数据一条一条流，内存里始终只有当前一条；10GB 日志照样跑"""

# 模拟原始日志（真实场景就是 open() 的文件对象——5.1 的 for line in f 走的正是同一套协议）
LOG_LINES = [
    "2026-10-18 10:00:01 INFO /login 200 35ms",
    "2026-10-18 10:00:02 ERROR /pay 500 1200ms timeout",
    "2026-10-18 10:00:03 INFO /query 200 42ms",
    "2026-10-18 10:00:04 ERROR /pay 500 1300ms timeout",
    "2026-10-18 10:00:05 ERROR /order 502 bad-gateway",
    "2026-10-18 10:00:06 INFO /login 200 30ms",
]


def read_lines(lines):
    """第 1 层 数据源：逐条吐出原始行"""
    for line in lines:
        parts = line.split()
        print(f"    [read] 产出: {parts[2]} {parts[3]}")
        yield line


def filter_errors(lines):
    """第 2 层 过滤：只放行 ERROR 行"""
    for line in lines:
        if "ERROR" in line:
            print(f"    [filter] 放行: {line.split()[3]}")
            yield line


def extract_fields(lines):
    """第 3 层 加工：切出接口、状态码、原因"""
    for line in lines:
        parts = line.split()
        report = f"{parts[3]} [{parts[4]}] {' '.join(parts[5:])}"
        print(f"    [extract] 加工: {parts[3]}")
        yield report


# 管道组装：三层只是套在一起，此时一条数据都没动（惰性到底）
pipeline = extract_fields(filter_errors(read_lines(LOG_LINES)))
print("管道已组装——注意上面没有任何 [read] 输出：数据还没开始加工")
print()

# for 拉第一个，数据才逐条穿过三层（看 trace 的交错顺序！）
print("错误报告:")
for report in pipeline:
    print(f"  >> {report}")
