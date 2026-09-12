

num1 = float(input("第一个数字："))
num2 = float(input("第二个数字："))
print("=" * 25)
print(num1,"+",num2,"=",f"{num1 + num2:.2f}")
print(num1,"-",num2,"=", f"{num1 - num2:.2f}")
print(num1,"*",num2,"=",f"{num1 * num2:.2f}")
if num2:
    print(num1,"/",num2,"=",f"{num1 / num2:.2f}")
    print(num1,"//",num2,"=",f"{num1 // num2:.2f}")
    print(num1, "%", num2, "=", f"{num1 % num2:.2f}")
    print(num1, "**", num2, "=", f"{num1 ** num2:.2f}")
    print("本次计算: [PASS]")
else:
    print(num1,"/",num2,"=","错误：除数不能为0")
    print(num1, "//", num2, "=", "错误：除数不能为0")
    print(num1, "%", num2, "=", "错误：除数不能为0")
    print(num1, "**", num2, "=", f"{num1 ** num2:.2f}")
    print("本次计算: [PARTIAL]")


print("=" * 25)
