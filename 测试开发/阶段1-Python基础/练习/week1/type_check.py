# 模拟接口返回的原始数据（全是字符串）
response_data = {
    "status_code": "200",
    "user_id": "10086",
    "balance": "99.5",
    "is_vip": "True"
}

print(f"status_code 是整数吗? {isinstance(response_data['status_code'],int)}")
response_data["status_code"] = int(response_data["status_code"])
response_data["user_id"] = int(response_data["user_id"])
response_data["balance"] = float(response_data["balance"])
print(f"转换后 status_code 是整数吗?{isinstance(response_data['status_code'],int)}")
print(f"转换后 balance 是浮点数吗? {isinstance(response_data['balance'],float)}")

log = f"[测试报告] 用户{response_data['user_id']} - 状态码:{response_data['status_code']} - 余额:{response_data['balance']}元 - VIP:{response_data['is_vip']}"


