password = 'test123'
count = 0
total_count = 3  # 最多输入密码次数
# 使用While可以在密码正确后就推出循环，for必须执行完所有循环
while count < total_count:
    in_password = input("密码：")
    count += 1
    if in_password != password:
        print(f"❌ 密码错误，还剩 {total_count - count} 次机会")
        if count == total_count:
            print("🔒 账户已锁定")
    else:
        print("✅ 登录成功")
        break
