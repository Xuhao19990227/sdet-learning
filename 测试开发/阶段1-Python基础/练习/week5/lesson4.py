# 5.4 练习：流式用例日志分析器（迭代器 + 生成器 + 管道）——周练习『日志分析脚本』的骨架
# 结构：两个数据源 → P0Iterator 类 → 三层生成器函数 → 主流程（本题零 import，全是语言内置能力）

# 数据源 1：用例列表——每项是 (case_id, priority) 元组，P0 = 冒烟级必跑
CASES = [("TC001", "P0"), ("TC002", "P2"), ("TC003", "P0"), ("TC004", "P1"), ("TC005", "P0")]

# 数据源 2：接口回归原始日志（模拟逐行流入的数据；真实场景对应 open() 的文件对象）
# 字段按空格切分：[0]日期 [1]时间 [2]级别 [3]路径 [4]状态码 [5]耗时 [6]详情
RAW_LOG = [
    "2026-10-18 20:00:01 INFO /login 200 35ms",
    "2026-10-18 20:00:02 ERROR /pay 500 1200ms timeout",
    "2026-10-18 20:00:03 INFO /query 200 42ms",
    "2026-10-18 20:00:04 WARN /cart 200 850ms slow",
    "2026-10-18 20:00:05 ERROR /pay 500 1300ms timeout",
    "2026-10-18 20:00:06 ERROR /order 502 90ms bad-gateway",
    "2026-10-18 20:00:07 INFO /login 200 30ms",
    "2026-10-18 20:00:08 WARN /search 200 990ms slow",
]


class P0Iterator:
    """手写迭代器：只吐 P0 用例的 case_id（协议 = __iter__ 返自身 + __next__ 给值或 raise StopIteration）"""

    def __init__(self, cases):
        # index 记在实例上：迭代器自己记"走到哪了"——这正是"一次性"的根源（list 能反复 for 是因为每次新建迭代器）
        self.cases = cases
        self.index = 0

    def __iter__(self):
        # 协议第 1 条：for 拿到对象先调 iter() 要迭代器；自己就是迭代器，返回自身
        return self

    def __next__(self):
        # 协议第 2 条：每调一次交出一个值，取完 raise StopIteration（for 靠它优雅收尾，不算报错）
        while self.index < len(self.cases):
            case_id = self.cases[self.index][0]
            priority = self.cases[self.index][1]
            # 先前进再判断：不管是不是 P0，这条都已消费掉；是 P0 才 return，不是就留在循环里找下一个
            self.index += 1
            if priority == "P0":
                return case_id
        raise StopIteration

# ---- 三层生成器管道：读 → 滤 → 加工；每层都惰性，被上层 for 拉动才干一行活，内存里永远只有当前一行 ----

def read_lines(lines):
    """数据源层：逐行 yield（同构 5.1 的 for line in f；真实场景把 lines 换成文件对象即流式读）"""
    for line in lines:
        yield line


def filter_by_levels(lines, levels):
    """过滤层：只放行级别 in levels 的行——levels 参数驱动（导师边界会换 {"INFO"} 复验），禁写死"""
    for line in lines:
        parts = line.split()
        # 索引 2 = 级别字段（INFO/ERROR/WARN）
        if parts[2] in levels:
            yield line


def to_report(lines):
    """加工层：原始行 → 报告行，逐条 yield 不攒 list（f-string 格式逐字符按题目规格）"""
    for line in lines:
        parts = line.split()
        report = f"{parts[2]} {parts[3]} [{parts[4]}] {' '.join(parts[5:])}"
        yield report


if __name__ == "__main__":
    # ---- A 段：手写迭代器。for 背后 = iter() 拿迭代器 + 反复 next()，直到 StopIteration 收尾 ----
    print("=== A 手写迭代器: 只吐 P0 用例 ===")
    p0_iter = P0Iterator(CASES)
    for case_id in p0_iter:
        print(f"  {case_id}")
    # 一次性实证：index 已走到头，list() 再走协议立刻 StopIteration → 空列表
    print(f"  取完再 list(): {list(p0_iter)}")
    # --- B 段：三层管道。组装 ≠ 执行——pipeline 建好这一刻，三个函数体一行都没跑（惰性）----
    print("=== B 生成器管道: ERROR 与 WARN 流式报告 ===")
    pipeline = to_report(filter_by_levels(read_lines(RAW_LOG), {"ERROR", "WARN"}))
    print("  管道已组装，此时还没加工任何数据")
    # 拉动方向：for 每次 next 向 to_report 要一行 → 逐级向下传导到 read_lines（上层拉下层，不是下层推）
    report_count = 0
    for report in pipeline:
        report_count += 1
        print(f"  {report_count}. {report}")
    print(f"  共 {report_count} 条")
    # ---- C 段：生成器表达式 = 匿名的生成器，同样一次性：next 吃掉第 1 个，list 只收剩下 2 个 ----
    print("=== C 生成器表达式: 一次性演示 ===")
    smoke_ids = (f"SMK{i:03d}" for i in range(1, 4))
    print(f"  next 取第 1 个: {next(smoke_ids)}")
    print(f"  list 取剩下的: {list(smoke_ids)}")
    # 1.迭代器一次性机制，用列表，list是可迭代对象，每次for都新建一个迭代器
    # 2.0行，filter_by_levels，从上拉下来的，源头是read_lines
    # 3.一个是将整个列表存到内存里，另一个是取一个用一个丢一个，一个可以反复使用，另一个可以减少内存占用，数据量可控的情况下可以用list
