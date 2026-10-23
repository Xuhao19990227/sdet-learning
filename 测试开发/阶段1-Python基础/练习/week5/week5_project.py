# 第五周综合练习：测试运行日志分析器——五零件管道（读取/解析/过滤/分类/统计，各管一层）
# 覆盖：5.4 生成器管道 + 5.5 正则命名分组 + 5.6 strptime/timedelta，回收 5.1 文件读取、5.2 异常分工
import re
from datetime import datetime

# 模块级常量：全题共用一份，函数里不散落硬编码
LOG_PATH = "run_log.txt"  # 相对路径：运行工作目录必须是 week5
TIME_FMT = "%Y-%m-%d %H:%M:%S"  # strptime 的时间解析模板
TIMEOUT_SECONDS = 3  # 超时阈值：耗时「超过」3 秒算超时（恰好 3.0 算 OK）
LEVELS = ("ERROR", "WARN")  # 关注的日志级别：参数化驱动 filter_by_level
# 整行正则（5.5）：^...$ 首尾锚定，五个命名分组各取所需；
# 脏行匹配不上 → to_record 返回 None。compile 预编译：管道每行复用同一个编译产物
LINE_PATTERN = re.compile(
    r"^(?P<case_id>TC\d{3}) \| (?P<start>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r" \| (?P<end>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    r" \| (?P<level>[A-Z]+) \| (?P<module>\w+)$"
)


# A 部分（5.4+5.1）：逐行读文件的生成器——惰性拉动，不把整个文件攒进内存
def read_lines(path):
    with open(path, encoding="utf-8") as f:  # with 自动关闭；encoding 显式声明，不赌系统默认
        while True:
            line = f.readline()  # 一次读一行（常见错误：read() 会整读且 EOF 后返回 "" 造成死循环）
            if not line:  # 只有 EOF 返回 ""（中部空行返回 "\n"，不是空串）→ 循环的正常出口
                break
            line = line.rstrip("\n")  # 先去掉行尾换行符
            if line:  # 规格 A「空行不 yield」：空行 rstrip 后成 ""，假值，在这里被跳过
                yield line  # 一次交出一根非空字符串


# B 部分之一（5.5+5.6）：一行文本 → 结构化记录 dict（纯逻辑层，不捕任何异常）
def to_record(line):
    record = LINE_PATTERN.search(line)  # 匹配对象（^...$ 已锚定，search 等效整行匹配）
    if record is None:
        return None  # 格式不符：如实报告「认不出」，怎么处置是上层的事
    # group("组名") 按名取值；end - start 得 timedelta，total_seconds() 转 float 秒（5.6）；
    # strptime 失败抛 ValueError——故意不捕，冒泡给 parse_all（5.2 分工：底层只说实话）
    cost = (datetime.strptime(record.group("end"), TIME_FMT) - datetime.strptime(record.group("start"),
                                                                                 TIME_FMT)).total_seconds()
    # 组装记录 dict：键顺序与题目规格一致（case_id、level、module、cost）
    return {"case_id": record.group("case_id"), "level": record.group("level"), "module": record.group("module"),
            "cost": cost}


# B 部分之二（5.2）：批量层逐条接住异常——脏行 yield None，流程不中断
def parse_all(lines):
    for line in lines:  # 直接接 read_lines 的流：拉一行处理一行（生成器管道）
        try:
            rec = to_record(line)
        except ValueError:  # 精确捕获（禁裸 except）：只处理「时间解析失败」这一种情况
            rec = None
        yield rec  # 正常记录 yield dict，脏行 yield None——都流向下游


# C 部分（5.4）：按级别过滤——levels 参数驱动，不写死（5.4 原课教训）
def filter_by_level(records, levels):
    for record in records:
        if record is None:
            yield None  # 脏行不归级别过滤管：原样放行，计数责任在下游（思考题 1）
        else:
            if record["level"] in levels:
                yield record  # 级别命中：交给下游统计
            else:
                continue  # 级别不符：不 yield，即被过滤掉


# D 部分：四分类纯函数——NEGATIVE 是 5.6 思考题 3 里设计出的分类，在这里落地
def classify(cost):
    if cost < 0:  # start/end 写反 → 负耗时：异常数据有自己的出口
        return "NEGATIVE"
    elif cost > TIMEOUT_SECONDS:  # 用常量不手写 3；> 对应「超过」，恰好 3.0 不算超时
        return "TIMEOUT"
    else:
        return "OK"


# E 部分（5.4 Q3 回收）：单遍流式累加——边消费流边算，不先攒 list 再算
def to_stats(items):
    # 八个键与题目规格逐字符一致；max_case/max_cost 必须在此初始化：
    # 主流程取键时不能缺，空文件/全脏也靠它们打出「无 (0.0s)」
    report = {"total": 0, "skipped": 0, "timeout": 0, "negative": 0,
              "valid_sum": 0, "valid_count": 0, "max_case": "无", "max_cost": 0.0}
    for item in items:
        if item is None:  # 脏行：只数 skipped——total 语义是「非 None 记录数」，判断之后才计数
            report["skipped"] += 1
            continue
        report["total"] += 1
        # TIMEOUT：计入超时，同时参与平均与最大值——它是真实跑完了的慢用例
        if classify(item["cost"]) == "TIMEOUT":
            report["timeout"] += 1
            report["valid_sum"] += item["cost"]
            report["valid_count"] += 1
            if report["max_cost"] < item["cost"]:  # 仅当当前耗时更大才更新两个键（朴素 if 最好控）
                report["max_case"], report["max_cost"] = item["case_id"], item["cost"]
            continue
        # NEGATIVE：只计数，不参与 valid_sum/valid_count/max——异常不污染统计（5.6 Q3 的判断）
        if classify(item["cost"]) == "NEGATIVE":
            report["negative"] += 1
            continue
        # OK：正常用例，参与平均与最大值
        if classify(item["cost"]) == "OK":
            report["valid_sum"] += item["cost"]
            report["valid_count"] += 1
            if report["max_cost"] < item["cost"]:
                report["max_case"], report["max_cost"] = item["case_id"], item["cost"]
            continue
    return report  # 函数级、循环走完才 return——缩进若进循环体就永远执行不到（隐式返回 None）


# 主流程：三个生成器串成管道 read_lines → parse_all → filter_by_level，
# 末端 to_stats 一把拉动整条链——一行数据流过全程，没有任何中间 list；
# avg 有除零保护：valid_count 为 0（空文件/全脏/无匹配级别）时平均按 0.0 计
if __name__ == "__main__":
    items = filter_by_level(parse_all(read_lines(LOG_PATH)), LEVELS)
    stats = to_stats(items)
    avg = stats["valid_sum"] / stats["valid_count"] if stats["valid_count"] else 0.0
    print("--- 日志分析报告 ---")
    print(f"匹配记录: {stats['total']}")
    print(f"跳过脏行: {stats['skipped']}")
    print(f"超时: {stats['timeout']}")
    print(f"负耗时: {stats['negative']}")
    print(f"平均耗时: {avg:.1f}s")
    print(f"最耗时: {stats['max_case']} ({stats['max_cost']:.1f}s)")

    # ---------- 思考题 ----------
    # 1. None也是日志的一部分，应该也是用例执行生成的，不应该去掉，丢失了就统计的数据来源就不完整了
    # 2. 因为在统计之前已经把它过滤了，如果先统计再过滤，就没法统计到需要统计的数据了
    # 3. 单遍流式累加，不用缓存所有数据，节约内存，但不能反复使用，list可以反复使用但会更大地占用内存，
    #    如果是TOP3的话，就建一个列表存TOP3的数据，如果列表长度小于3，就直接加入列表，
    #    如果等于3，就与列表中最低的对比，大于列表里最低的就替换它
