# demo56_1.py — 5.6 KP1：datetime 对象与时间戳
from datetime import datetime

# --- 1) now()：拿到当前时间，类型是 datetime 对象 ---
now = datetime.now()
print("now type:", type(now).__name__)

# --- 2) 属性直接取年月日时分秒（全是 int，不用再去解析字符串）---
print("date part:", now.year, now.month, now.day)
print("time part:", now.hour, now.minute, now.second)

# --- 3) 构造指定时间：比如约定的发布窗口 ---
release = datetime(2026, 11, 1, 2, 30, 0)
print("release:", release)

# --- 4) 时间戳：1970-01-01 00:00:00 起的秒数（float），5.3 timer 用的就是它 ---
ts = release.timestamp()
print("timestamp:", ts)
# 时间戳可以转回 datetime（双向通行）
print("back to datetime:", datetime.fromtimestamp(ts))
