# demo55_1.py — 5.5 正则 KP1：三个入口函数与基本语法
# 场景：从一条日志里提取信息（测试开发日常）
import re

log = "2026-10-18 20:31:05 ERROR [pay_api] 连接网关超时, 重试3次"

# --- 1) match：只从字符串开头配，开头不匹配立即返回 None ---
m1 = re.match(r"\d{4}-\d{2}-\d{2}", log)
print("match 日期:", m1.group())      # 开头恰好是日期 -> 命中

m2 = re.match(r"ERROR", log)
print("match ERROR:", m2)             # 开头不是 ERROR -> None

# --- 2) search：扫描整个字符串，第一个命中就停 ---
m3 = re.search(r"ERROR", log)
print("search:", m3.group())

# --- 3) findall：把所有命中收进列表 ---
print("findall 数字串:", re.findall(r"\d+", log))

# --- {m,n} 精确次数：用例编号固定是 TC + 3 位数字 ---
cases = "TC001 通过, TC042 失败, TC7 编号不合规"
print("合规编号:", re.findall(r"TC\d{3}", cases))
