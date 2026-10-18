"""5.4 课内演示2：生成器函数——yield 替你自动实现迭代器协议
要点：调用不执行（惰性）；next() 跑到 yield 暂停；状态全保留；还是一次性"""
import sys

# --- 1) 暂停与恢复：函数体像一本夹了书签的书 ---
# yield vs return（面试高频）：
#   return：结束函数，带走一个值，一锤子买卖
#   yield：交出一个值，函数暂停，状态全保留，下次 next() 从暂停处继续


def demo_flow():
    print("  [生成器] 开始执行，走到第 1 个 yield 前")
    yield 1
    print("  [生成器] 恢复了，走到第 2 个 yield 前")
    yield 2
    print("  [生成器] 恢复了，即将走到结尾（没有 yield 可交了）")


gen = demo_flow()               # 注意：调用生成器函数不执行函数体！只拿到一个生成器对象
print("调用了 demo_flow()——上面没有任何 [生成器] 输出，函数体一行都没跑（惰性）")
print(f"第 1 次 next 取到: {next(gen)}")
print(f"第 2 次 next 取到: {next(gen)}")
try:
    next(gen)                   # 第 3 次：跑完剩余函数体，没有值可交
except StopIteration:
    print("第 3 次 next：函数体走到结尾，StopIteration（和迭代器同款收场）")

print()


# --- 2) 生成器天然是迭代器：demo1 三十行的 CaseIterator，这里三行搞定 ---
def count_cases(n):
    """产出 1~n 号用例编号"""
    i = 1
    while i <= n:
        yield f"TC{i:03d}"
        i += 1


counter_gen = count_cases(3)
print(f"iter(counter_gen) is counter_gen: {iter(counter_gen) is counter_gen}")
print("for 消费:", end=" ")
for case_id in count_cases(3):
    print(case_id, end=" ")
print()

print()


# --- 3) 无限序列：list 装不下，生成器随便产 ---
def case_id_forever():
    """无限用例编号生成器——while True + yield，要多少拿多少"""
    n = 1
    while True:
        yield f"TC{n:06d}"
        n += 1


forever = case_id_forever()
print(f"无限生成器取 3 个: {next(forever)}, {next(forever)}, {next(forever)}——按需取，永不爆内存")

print()

# --- 4) 生成器表达式：推导式 [] 改 ()（2.3 回调）---
ids_list = [f"TC{i:06d}" for i in range(1_000_000)]   # 列表推导式：100 万个一次全产，塞进内存
ids_gen = (f"TC{i:06d}" for i in range(1_000_000))    # 生成器表达式：一个都不先产，要时才产
print(f"100 万条的列表光容器: {sys.getsizeof(ids_list) / 1024 / 1024:.1f} MB（还不含字符串本身）")
print(f"100 万条的生成器对象: {sys.getsizeof(ids_gen)} 字节（跟数据量无关）")
print(f"生成器取第 1 个: {next(ids_gen)}，第 2 个: {next(ids_gen)}——真正算过的只有这 2 条")
