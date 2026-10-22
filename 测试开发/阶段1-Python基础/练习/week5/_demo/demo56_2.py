# demo56_2.py — 5.6 KP2：字符串 <-> datetime 互转（日志分析的核心）
import re
from datetime import datetime

# --- 1) strptime：字符串 -> datetime（p = parse 解析）---
# 格式串必须与目标字符串逐字符对应：%Y 四位年 %m 月 %d 日 %H 时(24) %M 分 %S 秒
log_time = "2026-10-18 20:31:05"
dt = datetime.strptime(log_time, "%Y-%m-%d %H:%M:%S")
print("parsed type:", type(dt).__name__)
print("hour:", dt.hour, "| weekday:", dt.weekday())  # weekday: 0=周一 ... 6=周日

# --- 2) 与 5.5 正则联动：先用分组抠出时间字段，再 strptime 解析 ---
line = "2026-10-18 20:31:05 ERROR [pay_api] 连接网关超时"
m = re.search(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
dt2 = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
print("regex + strptime:", dt2)


# --- 3) strftime：datetime -> 字符串（f = format 格式化），常用于生成报告文件名 ---
print("report name:", dt.strftime("report_%Y%m%d_%H%M%S.txt"))

# --- 4) 格式对不上 = ValueError（5.2 精确捕获正好用上）---
try:
    datetime.strptime("2026-10-18", "%Y-%m-%d %H:%M:%S")
except ValueError as e:
    print("ValueError:", e)
