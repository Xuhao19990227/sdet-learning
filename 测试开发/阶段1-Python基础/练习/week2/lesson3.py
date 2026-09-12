results = ["pass", "fail", "pass", "skip", "fail", "pass", "error", "pass", "fail", "pass"]
results.append("pass")
results.remove("error")
print(results)
print(len(results))
count = results.count("pass")

problems = [res for res in results if res != "pass"]
print(problems)
# 如果results是空列表，分母为0，计算报错
pass_rate = f"{count / len(results):.1%}" if results else "N/A"
print(pass_rate)

for i in range(len(results)):
    print(f"用例{i + 1}:", results[i])

# 分别是11，12；因为results.sort()是直接改变原列表，返回None

