# 5.6 用例耗时报告：strptime 解析时间字符串，timedelta 算耗时，strftime 生成文件名
from datetime import datetime

# 数据源：每行 = "用例编号 | 开始时间 | 结束时间"
# TC004 的结束时间是故意放的脏数据，用来测异常链路
CASE_RECORDS = [
    "TC001 | 2026-10-18 20:31:05 | 2026-10-18 20:31:07",
    "TC002 | 2026-10-18 20:31:10 | 2026-10-18 20:31:14",
    "TC003 | 2026-10-18 20:31:15 | 2026-10-18 20:31:18",
    "TC004 | 2026-10-18 20:32:00 | not_a_time",
]
TIME_FMT = "%Y-%m-%d %H:%M:%S"  # 时间格式模板：%Y年 %m月 %d日 %H时(24制) %M分 %S秒
TIMEOUT_SECONDS = 3  # 超时阈值（秒）：耗时「超过」3 秒才算 TIMEOUT，恰好 3.0 算 OK
LOG_TIME = datetime(2026, 10, 18, 20, 31, 5)  # 一个给定的日志时间点，供 D 部分生成报告文件名


# A 部分：把一行记录拆成结构化字典（纯逻辑层）
# 关键设计：本函数故意不捕任何异常——时间格式不对就让 ValueError 往上抛，
# 由调用方决定怎么处置（底层只说实话，分工见思考题 1）
def parse_record(record):
    # 固定分隔符 " | " 用 split 切三段：[0]编号 [1]开始 [2]结束
    case_id, start_time, end_time = record.split(" | ")
    # strptime(字符串, 格式模板)：按 TIME_FMT 把 "2026-10-18 20:31:05" 解析成 datetime 对象；
    # 字符串与模板对不上（如 "not_a_time"）就抛 ValueError
    return {"case_id": case_id, "start": datetime.strptime(start_time, TIME_FMT),
            "end": datetime.strptime(end_time, TIME_FMT)}


# B 部分：算一条记录的耗时（秒，float）；整条链路的异常在这一层统一接
def duration_seconds(record):
    try:
        parsed = parse_record(record)  # 脏数据会在 parse_record 里抛 ValueError，冒泡到这里
        cost = parsed["end"] - parsed["start"]
        # datetime 相减，得到 timedelta（时间差）对象
        return cost.total_seconds()  # timedelta 换算成总秒数（float）
    except ValueError:  # 精确捕获（禁裸 except）：只处理「时间解析失败」这一种情况
        return None  # 脏数据不让程序崩，返回 None 作标记，交给 classify 判成 ERROR


# C 部分：三分类纯函数；入参是 B 的返回值（float 或 None）
def classify(cost):
    if cost is None:  # None 说明这条记录解析不出来（脏数据）
        return "ERROR"
    elif cost > TIMEOUT_SECONDS:  # 耗时超过阈值 → 超时（注意规格用 > 而不是 >=）
        return "TIMEOUT"
    else:  # 其余所有值（≤ TIMEOUT_SECONDS，含负数——见思考题 3 实验）→ OK
        return "OK"


# D 部分：strftime 反向操作——把 datetime 对象格式化成字符串（拼报告文件名）
def make_report_name(dt):
    # %Y%m%d_%H%M%S 全部自动补零，如 1 月 2 日 → 0102
    return dt.strftime("report_%Y%m%d_%H%M%S.txt")


# 主流程：__name__ 防护——只有「直接运行」才执行报告；被别的模块 import 时不自动跑（无副作用）
if __name__ == "__main__":
    print("--- 耗时报告 ---")
    for record in CASE_RECORDS:
        cost = duration_seconds(record)  # 脏行返回 None，不崩
        # 注意：这里取 case_id 用 split 而不是 parse_record——parse_record 对脏行会抛异常，
        # 连编号都拿不到；split 永远切得动，所以 ERROR 行也能带着编号打出来（思考题 1）
        case_id = record.split(" | ")[0]
        print(case_id, classify(cost), cost)
    print("--- 报告文件名 ---")
    print(make_report_name(LOG_TIME))

    # 1.这个会导致定位不到里层的错误，错误会体现在调用层
    # 2，超过；看需求吧
    # 3.推理：始/末写反后 end - start 得到负的 timedelta，total_seconds() 返回负数；
    #   推理：负数既不是 None，也不会大于 TIMEOUT_SECONDS，所以必落 else 分支，classify 判成 OK
    #   实验：把 CASE_RECORDS 三条合法记录的始/末时间互换后运行主流程，输出如下（实验后数据已还原）：
    # --- 耗时报告 ---
    # TC001 OK -2.0
    # TC002 OK -4.0
    # TC003 OK -3.0
    # TC004 ERROR None
    # --- 报告文件名 ---
    # report_20261018_203105.txt
    # 不合理，因为耗时不可能是负数，我会在classify这个函数给耗时小于0的单独返回一个字符串，标志为耗时为负数的错误
