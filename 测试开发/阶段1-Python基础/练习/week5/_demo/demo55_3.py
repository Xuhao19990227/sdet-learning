# demo55_3.py — 5.5 正则 KP3：分组提取 + re.compile 复用
import re

logs = [
    "2026-10-18 20:31:05 ERROR [pay_api] 连接网关超时",
    "2026-10-18 20:31:06 INFO [user_api] 登录成功",
    "2026-10-18 20:31:07 ERROR [pay_api] 状态码500",
]

# --- 1) 分组：每对 () 是一个捕获组 ---
# 组1=日期 组2=时间 组3=级别 组4=模块 组5=消息
pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)"

print("--- search + group 逐组取 ---")
m = re.search(pattern, logs[0])
print("group(0) 整个命中:", m.group(0))
print("group(3) 级别:", m.group(3))
print("group(4) 模块:", m.group(4))
print("groups() 全部组:", m.groups())

# --- 2) findall 带分组：返回元组列表，每组一个元素 ---
print("\n--- findall 只提取 级别+模块 ---")
pairs = re.findall(r"(\w+) \[(\w+)\]", "\n".join(logs))
for level, module in pairs:          # 元组解包（呼应 5.4 建议）
    print(level, module)

# --- 3) re.compile：模式编译一次，反复用（大量日志时更快） ---
print("\n--- compile 复用，只挑 ERROR 行 ---")
error_pat = re.compile(r"ERROR \[(\w+)\] (.+)")
for line in logs:
    m2 = error_pat.search(line)
    if m2:
        print("模块:", m2.group(1), "| 消息:", m2.group(2))

# --- 4) 命名分组 (?P<name>...)：给组起名字，可读性更好 ---
print("\n--- 命名分组 ---")
named = re.compile(r"(?P<level>\w+) \[(?P<module>\w+)\]")
m3 = named.search(logs[0])
print("按名字取:", m3.group("level"), m3.group("module"))
