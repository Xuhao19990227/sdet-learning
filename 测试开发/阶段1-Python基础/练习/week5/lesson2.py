import csv
class ApiNotFoundError(Exception):
    """自定义异常：接口路径不存在"""


def fake_api(api):
    """模拟接口 v2：未知路径抛自定义异常"""
    responses = {
        "/login": {"status_code": 200, "msg": "success"},
        "/pay": {"status_code": 500, "msg": "server error"},
        "/order": {"status_code": 200, "msg": "success"},
        "/cart": {"status_code": 200, "msg": "success"},
        "/logout": {"status_code": 200, "msg": "success"},
    }
    if api not in responses:
        raise ApiNotFoundError(f"未知接口路径: {api}")
    return responses[api]


if __name__ == '__main__':
    with open('dirty_cases.csv', newline='', encoding='utf-8') as f:
        cases = csv.DictReader(f)
        results = []
        for case in cases:
            try:
                expected_status = int(case["expected_status"])
                expected_msg = case["expected_msg"]
                response = fake_api(case['api'])
            except ApiNotFoundError:
                result = {
                    "case_id": case["case_id"],
                    "status": "ERROR(接口不存在)"
                }
            except ValueError:
                result = {
                    "case_id": case["case_id"],
                    "status": "ERROR(数据非法)"
                }
            else:
                status = expected_status == response["status_code"] and expected_msg == response["msg"]
                result = {
                    "case_id": case["case_id"],
                    "status": "PASS" if status else "FAIL"
                }
            finally:
                results.append(result)
    for result in results:
        print(result["case_id"], result["status"])
    total = len(results)
    passed = len([result for result in results if result["status"] == "PASS"])
    failed = len([result for result in results if result["status"] == "FAIL"])
    errored = total - (passed + failed)
    print(f"共 {total} 条: PASS {passed}, FAIL {failed}, ERROR {errored}")

    # 1. 异常首先体现在浅层的调用，再深入体现再调用的函数内部，中间层不需要写处理代码，意味着纯逻辑类不需要写处理异常的代码
    # 2.因为这样写是捕获所有类型的错误，不方便定位bug，比如我代码的键写错了
    # 3.else是没有错误才执行的代码，如果直接写在后面，就是无论是否错误都会执行，相当于finally了
