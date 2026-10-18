"""5.3 课内演示2b：反面教材——不加 @wraps 会怎样"""
import time

def timer_bad(func):
    """功能与 timer 完全相同，唯独少了 @wraps(func)"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        cost = (time.time() - start) * 1000
        print(f"[timer] {func.__name__} 耗时 {cost:.1f} ms")
        return result
    return wrapper

@timer_bad
def test_search():
    """搜索接口用例"""
    time.sleep(0.05)
    return "PASS"

print(test_search())
print("名字:", test_search.__name__)       # wrapper——test_search 不见了！
print("文档:", test_search.__doc__)        # None——用例说明也丢了！
