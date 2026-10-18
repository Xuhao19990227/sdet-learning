"""5.3 课内演示2：基础装饰器——不改用例代码，给它加计时"""
import time
from functools import wraps

def timer(func):
    """装饰器：收原函数，返回"包了计时"的新函数"""
    @wraps(func)                          # 把原函数的身份证搬给 wrapper
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)    # 原函数体照常执行，一行没改
        cost = (time.time() - start) * 1000
        print(f"[timer] {func.__name__} 耗时 {cost:.1f} ms")
        return result
    return wrapper

def test_login():
    """登录接口用例"""
    time.sleep(0.2)      # 模拟 200ms 网络请求
    return "PASS"

# --- 手动装配：看清 @ 背后的那行代码 ---
test_login = timer(test_login)
print(test_login())                          # PASS，且多了计时输出
print("装配后名字:", test_login.__name__)    # test_login（@wraps 保住了）

# --- 语法糖版：与上面手动那行完全等价 ---
@timer
def test_pay():
    """支付接口用例"""
    time.sleep(0.1)
    return "FAIL"

print(test_pay())
print("名字:", test_pay.__name__)            # test_pay
print("文档:", test_pay.__doc__)             # 支付接口用例
