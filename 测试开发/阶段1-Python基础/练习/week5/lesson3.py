import time
from functools import wraps

api_state = {"query_calls": 0}


def fake_api(path):
    """模拟接口 v3：/query 是抖动接口——前 2 次调用返回 500，第 3 次起返回 200"""
    if path == "/query":
        api_state["query_calls"] += 1
        if api_state["query_calls"] <= 2:
            return 500
        return 200
    codes = {"/login": 200, "/pay": 500}
    return codes.get(path, 404)


def timer(func):
    """计时装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
        finally:
            cost = (time.time() - start) * 1000
            print(f"[timer] {func.__name__} 耗时 {cost:.1f} ms")
        return result

    return wrapper


def call_counter(func):
    """统计调用次数装饰器"""
    counter = {"n": 0}

    @wraps(func)
    def wrapper(*args, **kwargs):
        counter['n'] += 1
        print(f"[count] {func.__name__} 累计调用 {counter['n']} 次")
        result = func(*args, **kwargs)
        return result

    return wrapper


def retry(times):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    print(f"[retry] {func.__name__} 第 {attempt} 次失败: {e}")
            raise AssertionError(f"{func.__name__} 重试 {times} 次仍失败")

        return wrapper

    return decorator


@timer
@call_counter
@retry(times=3)
def run_case(case_id, path, expected_status):
    """单条用例校验：请求 fake_api，断言状态码"""
    actual = fake_api(path)
    assert actual == expected_status, f"{case_id} {path} 期望 {expected_status} 实际 {actual}"
    return f"{case_id} PASS"


if __name__ == "__main__":
    print("=== TC001 稳定接口: 一次通过 ===")
    result = run_case("TC001", "/login", 200)
    print(f"结果: {result}")

    print("=== TC002 抖动接口: 重试 2 次后成功 ===")
    result = run_case("TC002", "/query", 200)
    print(f"结果: {result}")

    print("=== TC003 永败接口: 重试用尽仍失败 ===")
    try:
        run_case("TC003", "/pay", 200)
    except AssertionError as e:
        print(f"浅层捕获: {e}")

    # 1.因为[count]在[retry]的外层，换了位置的话，retry打多少行count就打多少行
    # 2.用的finally,会少打印耗时，如果是性能测试，接口响应超时，也可以知道失败的原因
    # 3.失败重试解决了环境问题导致的失败，可能会掩盖掉性能问题，我觉得需要分析之前执行失败的原因是什么
