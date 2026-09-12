response = {
    "code": 200,
    "message": "success",
    "data": {
        "total": 3,
        "users": [
            {"id": 1, "name": "张三", "role": "admin", "score": 92},
            {"id": 2, "name": "李四", "role": "tester", "score": 78},
            {"id": 3, "name": "王五", "role": "dev", "score": 85}
        ]
    }
}

code = response["code"]
message = response["message"]
if code == 200:
    print("接口调用成功")
else:
    print(f"接口异常：{message}")

total = response["data"]["total"]
print(f"共 {total} 条数据")

users = response["data"]["users"]
for user in users:
    print(user["name"], "-", user["role"])
sor_users = sorted(users, key=lambda x: x["score"], reverse=True)

print(f"最高分：{sor_users[0]['name']}（{sor_users[0]['score']}分）")

page_info = response.get("data", {}).get("page_info", "无分页信息")
print(page_info)

user_names = [user["name"] for user in users if user["role"] in ("admin", "dev")]

print(user_names)

# 如果users是空列表[],我的第四题会报错indexerror,可以先用if判断，有值再取
