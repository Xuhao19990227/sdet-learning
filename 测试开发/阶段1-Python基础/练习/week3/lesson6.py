from test_utils import is_success
import test_utils

results = ["PASS", "FAIL", "PASS", "SKIP", "FAIL"]
codes = [200, 201, 404, 500]

print("当前环境配置:", test_utils.load_config(env='test'))
print("状态统计:", test_utils.count_by_status(results))

for code in codes:
    print(f"{code} → {'成功' if is_success(code) else '失败'}")

print(f"test_utils 的 __name__ = {test_utils.__name__}")
print(f"本文件的 __name__ = {__name__}")
