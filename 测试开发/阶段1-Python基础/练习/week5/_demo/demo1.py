"""5.3 课内演示1：函数是一等公民——能赋值、能当参数、能当返回值"""

def fake_api(path):
    """假接口：按路径发状态码"""
    codes = {"/login": 200, "/pay": 500}
    return codes.get(path, 404)

# --- 1) 函数能赋值给变量：赋的是"名片"，加括号才是"值" ---
check = fake_api
print(check("/login"))         # 200，别名照样能调用
print(fake_api("/unknown"))    # 404

# --- 2) 函数能当参数传（回调）：3.7 的 map/filter 早就这么干 ---
def run_with_log(func, path):
    """执行器：调用 func 前后加日志"""
    print(f"[LOG] 即将请求 {path}")
    result = func(path)
    print(f"[LOG] 请求结束，状态码 {result}")
    return result

run_with_log(fake_api, "/pay")

# --- 3) 函数能返回函数（函数工厂） ---
def make_checker(expected):
    """生产一个只认 expected 的检查器函数"""
    def checker(actual):
        return actual == expected
    return checker

is_200 = make_checker(200)
print(is_200(fake_api("/login")))    # True
print(is_200(fake_api("/pay")))      # False
