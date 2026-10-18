"""5.3 课内演示2c：身份证是谁的属性——函数对象自己的"""

# 函数一等公民（KP1）：函数也是对象，对象就有属性
def test_login():
    """登录接口用例"""
    return "PASS"

print("--- def 那一刻，Python 自动填好的三张证 ---")
print("名字:", test_login.__name__)      # def 后面那个名字
print("文档:", test_login.__doc__)       # def 下第一行字符串
print("模块:", test_login.__module__)    # def 被执行时所在的模块


def deco(func):
    def wrapper(*args, **kwargs):
        """我是 wrapper 自己的文档"""
        return func(*args, **kwargs)
    return wrapper


decorated = deco(test_login)
print("--- 装饰后：名字绑到了另一个函数对象上 ---")
print("是同一个对象吗:", decorated is test_login)  # False
print("名字:", decorated.__name__)                 # wrapper 出生时的名字
print("文档:", decorated.__doc__)                  # wrapper 自己的文档
print("模块:", decorated.__module__)               # 在哪个模块里 def 的 wrapper

print("--- 原函数对象一点没变，只是你手里的名字不再指向它 ---")
print("名字:", test_login.__name__)
print("文档:", test_login.__doc__)
