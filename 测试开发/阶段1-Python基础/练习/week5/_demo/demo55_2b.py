# demo55_2b.py — 5.5 KP2 补充：贪婪 vs 懒惰，引擎怎么走
import re

s = "<a>b</a>"
print("原字符串:", s)

# 贪婪：.+ 先吃到底再回退 -> 命中到最后一个 >
greedy = re.search(r"<.+>", s)
print("贪婪 <.+>  命中:", greedy.group())   # <a>b</a> 整串

# 懒惰：.+? 先吃一口，够用就停 -> 命中到第一个 >
lazy = re.search(r"<.+?>", s)
print("懒惰 <.+?> 命中:", lazy.group())     # <a> 第一对

print("-" * 30)

# 换成日志场景更直观：抓中括号里的内容
log = "[pay_api] [user_api]"
print("日志:", log)

# 贪婪：从第一个 [ 吃到最后一个 ]
print("贪婪 \\[.+\\] :", re.findall(r"\[.+\]", log))
# 懒惰：每对 [] 单独抓
print("懒惰 \\[.+?\\]:", re.findall(r"\[.+?\]", log))
