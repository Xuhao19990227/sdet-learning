# demo55_2.py — 5.5 正则 KP2：贪婪 vs 懒惰、锚点
import re

# --- 1) 贪婪：默认能多吃就多吃 ---
s = "a1b2c3d"
# \w+ 会一口气吃到不能再吃为止
print("贪婪 \\w+:", re.findall(r"\w+", s))       # 整串一个命中
# \w+? 懒惰，每次只吃 1 个
print("懒惰 \\w+?:", re.findall(r"\w+?", s))     # 每个字符一个命中

# --- 2) 经典翻车：抓 HTML/日志里的成对标签 ---
html = "<b>bold</b><i>it</i>"
print("贪婪 <.+>:", re.findall(r"<.+>", html))   # 从第一个< 吃到最后一个>，整串一个命中
print("懒惰 <.+?>:", re.findall(r"<.+?>", html)) # 每遇到一个 > 就收手，四个标签各自命中

# --- 3) 锚点：^ 开头，$ 结尾 ---
line1 = "ERROR: disk full"
line2 = "WARN: disk almost full ERROR"
print("^ERROR 命中:", re.findall(r"^ERROR", line1))  # 命中
print("^ERROR 命中:", re.findall(r"^ERROR", line2))  # 空，ERROR 不在开头
print("full$ 命中:", re.findall(r"full$", line1))   # 命中，full 在结尾

# --- 4) 多行模式 re.M：让 ^ $ 对每一行生效 ---
multi = "INFO start\nERROR boom\nINFO end"
print("每行 ^ERROR (re.M):", re.findall(r"^ERROR", multi, re.M))
