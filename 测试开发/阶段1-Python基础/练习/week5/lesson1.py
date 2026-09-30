import csv
import json


def fake_api(api):
    """模拟接口：按路径返回固定响应"""
    responses = {
        "/login": {"status_code": 200, "msg": "success"},
        "/pay": {"status_code": 500, "msg": "server error"},
        "/order": {"status_code": 200, "msg": "success"},
        "/cart": {"status_code": 200, "msg": "success"},
        "/logout": {"status_code": 200, "msg": "success"},
    }
    return responses[api]


if __name__ == '__main__':
    with open("cases.csv", newline="", encoding="utf-8") as f:
        cases = csv.DictReader(f)
        results = []
        for case in cases:
            response = fake_api(case["api"])
            result = "PASS" if response["status_code"] == int(case["expected_status"]) and response["msg"] == case[
                "expected_msg"] else "FAIL"
            results.append({"case_id": case["case_id"], "status": result})
            print(f"{case['case_id']} {result}")
        print(f"通过 {len([r for r in results if r['status'] == 'PASS'])}/{len(results)}")
        report = {"total": len(results),
                  "passed": len([r for r in results if r['status'] == 'PASS']),
                  "results": results
                  }
    with open("report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
