# 演示：read_lines 原写法的问题（学生原版代码，一字未改）
# 问题1：f.read() 是「一次读整个文件」，不是读一行 → 第一次 yield 出来的是整个文件的内容
# 问题2：读到 EOF 后 f.read() 永远返回 ""，走 else: continue → 死循环，生成器永远卡住
# 运行方式：timeout 5 python demo_read_lines_bug.py sample_lines.txt
# 预期：打出第一次 next() 的结果后卡死，5 秒被 timeout 杀掉（退出码 124）
import sys


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        while True:
            line = f.read().strip("\n")
            if line:
                yield line
            else:
                continue


if __name__ == "__main__":
    gen = read_lines(sys.argv[1])  # 命令行参数：样例文件路径
    first = next(gen)
    print("第 1 次 next() 拿到:", repr(first))
    print("↑ 这不是「一行」，是整个文件的内容（内部的 \\n 都还在）")
    print("准备第 2 次 next()：已到 EOF，read() 永远返回 ''，else: continue 死循环，会永远卡住...")
    second = next(gen)
    print("第 2 次 next() 拿到:", repr(second))  # 永远执行不到这一行
