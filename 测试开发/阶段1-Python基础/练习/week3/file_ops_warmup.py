def write_logs(path, logs):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(logs)


def analyze_log(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]
        total = len(lines)
        errors = []
        for n, line in enumerate(lines, start=1):
            if "ERROR" in line:
                errors.append((n, line))
        return {'total': total, 'errors': errors}


logs = '''2026-09-12 21:00:01 INFO 服务启动成功
2026-09-12 21:00:03 INFO 加载配置文件 config.yaml
2026-09-12 21:00:07 ERROR 数据库连接超时: 重试 1
2026-09-12 21:00:12 INFO 收到请求 POST /api/login
2026-09-12 21:00:15 ERROR 接口 /api/pay 返回 500
2026-09-12 21:00:20 WARN 响应时间 2.3s 超过阈值
2026-09-12 21:00:25 ERROR 数据库连接超时: 重试 2
'''
write_logs('server.log', logs)
analyze = analyze_log("server.log")
print(f"日志分析完成: 共 {analyze['total']} 条, 其中 ERROR {len(analyze['errors'])} 条")
for error in analyze['errors']:
    print(f"第{error[0]}行: {error[1]}")

with open("report.txt", 'w', encoding='utf-8') as f:
    f.write("日志分析报告\n")
    f.write(f"总日志数: {analyze['total']}\n")
    f.write(f"ERROR 数量: {len(analyze['errors'])}\n")
    f.write("ERROR 明细:\n")
    for n, line in analyze["errors"]:
        f.write(f"第{n}行: {line}\n")

with open("report.txt", 'r', encoding='utf-8') as f:
    print("\n--- report.txt 内容 ---")
    for line in f:
        print(line.strip())

# 运行第二次会在文件结尾追加写入一样的内容；使用'w'第二次会覆盖掉第一次运行写的内容
# 不写会显示乱码
# enumerate函数
