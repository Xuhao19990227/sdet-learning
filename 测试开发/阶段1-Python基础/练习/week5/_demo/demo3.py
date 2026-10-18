"""5.3 课内演示3：带参装饰器——失败自动重试（三层结构）"""
from functools import wraps

def retry(times):
    """第一层：收装饰器参数，返回真正的装饰器"""
    def decorator(func):
        """第二层：收被装饰的函数，返回包装版"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """第三层：收调用参数，真正执行"""
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)    # 成功就直接返回，不再重试
                except AssertionError as e:
                    print(f"[retry] 第 {attempt} 次失败: {e}")
            # 循环走完还没 return = times 次全失败，异常照抛（5.2 的旅行）
            raise AssertionError(f"{func.__name__} 重试 {times} 次仍失败")
        return wrapper
    return decorator

attempts = {"count": 0}        # 用字典记次数，避免 global

@retry(times=3)
def test_flaky():
    """不稳定用例：第 3 次才通过"""
    attempts["count"] += 1
    n = attempts["count"]
    assert n >= 3, f"第 {n} 次仍失败"

print("名字:", test_flaky.__name__)    # test_flaky
test_flaky()                           # 前 2 次失败，第 3 次成功
print("最终结果: 测试通过")

# --- 重试用尽仍失败：异常照常抛出，浅层照样能接 ---
@retry(times=2)
def test_always_fail():
    """永远失败的用例"""
    assert False, "接口返回 500"

try:
    test_always_fail()
except AssertionError as e:
    print("浅层捕获:", e)
