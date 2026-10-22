# demo56_3.py — 5.6 KP3：时间运算 timedelta（耗时统计 / 比较 / 推算）
import time
from datetime import datetime, timedelta

start = datetime.strptime("2026-10-18 20:31:05", "%Y-%m-%d %H:%M:%S")
end = datetime.strptime("2026-10-18 20:31:07", "%Y-%m-%d %H:%M:%S")

# --- 1) datetime 相减 = timedelta（5.3 timer 装饰器算耗时的 datetime 版）---
cost = end - start
print("cost:", cost, "=", cost.total_seconds(), "seconds")

# --- 2) 加减 timedelta：推算未来/过去的时间点，比如 token 有效期 ---
expire = end + timedelta(minutes=30)
print("expire:", expire)
yesterday = end - timedelta(days=1)
print("yesterday:", yesterday)

# --- 3) 比较：datetime 直接 > < ==，可做"是否超时"断言 ---
print("timeout(>1s):", cost > timedelta(seconds=1))
print("start < end:", start < end)

# --- 4) time 模块两件套（5.3 timer 同款）：time.time() 打点、time.sleep() 等待 ---
t0 = time.time()
time.sleep(0.1)
print("slept:", round(time.time() - t0, 3), "seconds")
