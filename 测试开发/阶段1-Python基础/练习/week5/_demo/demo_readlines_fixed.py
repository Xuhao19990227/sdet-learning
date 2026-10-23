# read_lines 的两种正确写法（对照 demo_read_lines_bug.py）
# 写法1：read() 换成 readline()——每次只读一行
#   关键区别：EOF 时 readline() 返回 ""（空串）；文件中部的空行返回 "\n"（不是空串）
#   所以必须「先判 EOF 再 strip」：if not line: break
# 写法2（更 Pythonic）：直接 for line in f
#   文件对象本身就是迭代器（5.4 学的）：for 自动调 next()，EOF 自动结束循环
#   根本不需要 while True / break / continue
import sys


def read_lines_readline(path):
    with open(path, encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:  # 只有 EOF 会返回空串 "" → 循环的正常出口
                break
            yield line.rstrip("\n")  # rstrip 只去掉末尾换行；strip 会连开头的空白一起删


def read_lines_for(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


if __name__ == "__main__":
    p = sys.argv[1]
    print("readline 版（注意空行被保留为 ''）:")
    for item in read_lines_readline(p):
        print(repr(item))
    print("for 版（结果完全一致）:")
    for item in read_lines_for(p):
        print(repr(item))
