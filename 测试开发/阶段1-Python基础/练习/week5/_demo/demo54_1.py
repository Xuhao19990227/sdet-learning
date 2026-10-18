"""5.4 课内演示1：迭代器协议——2.2 就用熟的 for 循环，今天拆它的内脏
要点：可迭代对象有 __iter__；迭代器还要有 __next__；StopIteration 是收尾信号"""

# --- 1) 手动迭代：for 循环其实是三步流水线 ---
cases = ["TC001", "TC002", "TC003"]

it = iter(cases)                # 第 1 步：iter() 向可迭代对象要一个迭代器（实际调用 cases.__iter__()）
print(next(it))                 # 第 2 步：next() 取一个（实际调用 it.__next__()）
print(next(it))
print(next(it))
try:
    print(next(it))             # 第 3 步：数据取完，再要就抛 StopIteration
except StopIteration:
    print("StopIteration：取完的信号——for 循环默默接住它收尾，所以平时看不见报错")

print()

# --- 2) 可迭代对象 vs 迭代器：一字之差，两个东西（面试高频）---
print(f"list 是可迭代对象: {hasattr(cases, '__iter__')}")
print(f"list 本身不是迭代器: {hasattr(cases, '__next__')}")
print(f"iter() 返回的才是迭代器: {hasattr(it, '__next__')}")
print(f"对迭代器再调 iter() 返回它自己: {iter(it) is it}")

print()

# --- 3) for 循环手动展开：两种写法完全等价 ---
for case_id in cases:
    print(f"for 版: {case_id}")

it2 = iter(cases)
while True:
    try:
        case_id = next(it2)
        print(f"展开版: {case_id}")
    except StopIteration:
        break

print()

# --- 4) 手写迭代器类：用例套件迭代器（4.5 魔术方法家族添两个新成员）---
class CaseIterator:
    """逐条吐出用例编号——实现迭代器协议，for 就能消费它"""

    def __init__(self, case_ids):
        self.case_ids = case_ids
        self.index = 0

    def __iter__(self):
        # 协议第 1 条：__iter__ 返回迭代器自身
        return self

    def __next__(self):
        # 协议第 2 条：每次吐一个；取完抛 StopIteration
        if self.index >= len(self.case_ids):
            raise StopIteration
        case_id = self.case_ids[self.index]
        self.index += 1
        return case_id


suite = CaseIterator(["TC101", "TC102", "TC103"])
for case_id in suite:           # 自定义对象照样能 for——只要实现了协议
    print(f"自定义迭代器: {case_id}")

# --- 5) 大坑：迭代器是一次性的（list 可反复 for，迭代器不行）---
print(f"suite 已取完，再 list() 一次: {list(suite)}")   # 空列表！index 状态记在实例上
suite2 = CaseIterator(["TC201", "TC202"])
print(f"换个新迭代器才有货: {list(suite2)}")            # list() 内部同样走协议逐个 next()
