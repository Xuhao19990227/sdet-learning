import re  # 正则表达式模块：文本提取、格式校验的核心工具

# 模拟接口测试中常见的日志行：日期 时间 级别 [模块] 消息
LOG_LINES = [
    "2026-10-18 20:31:05 ERROR [pay_api] 连接网关超时",
    "2026-10-18 20:31:06 INFO [user_api] 登录成功",
    "2026-10-18 20:31:07 ERROR [pay_api] 状态码500",
    "2026-10-18 20:31:08 WARN [order_api] 响应慢2.3秒",
]

CASE_TEXT = "TC001 通过, TC042 失败, TC7 编号不合规, TC123 复测通过"
MODULE_TEXT = "错误来自 [pay_api] [user_api]"
# 预编译日志行模式（compile 后复用更快），5 个括号 = 5 个捕获分组：
#   (\d{4}-\d{2}-\d{2})  分组1 日期，如 2026-10-18
#   (\d{2}:\d{2}:\d{2})  分组2 时间，如 20:31:05
#   (\w+)                分组3 日志级别，如 ERROR / INFO / WARN
#   \[(\w+)\]            分组4 模块名（\[ \] 匹配字面方括号，只捕获里面内容）
#   (.+)                 分组5 消息正文（.+ 贪婪匹配到行尾）
# ^...$ 锚定整行：从头到尾必须完全符合该格式
LINE_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) \[(\w+)\] (.+)$")


def extract_case_ids(text):
    """从测试报告文本中提取合规的用例编号（TC + 恰好3位数字）"""
    # TC\d{3}：字面量 TC 后跟 3 位数字；TC7 只有 1 位数字，不匹配 → 被判"编号不合规"
    case_ids = re.findall(r"TC\d{3}", text)  # findall 返回所有匹配的列表
    return case_ids


def parse_line(line):
    """把一行日志解析成字典；格式不符返回 None"""
    parse = LINE_PATTERN.search(line)  # 不匹配时 search 返回 None，而不是抛异常
    try:
        # 对 None 调 .group() 会抛 AttributeError，这里借异常兜底处理不合规行
        line_dict = {"date": parse.group(1), "time": parse.group(2), "level": parse.group(3), "module": parse.group(4),
                     "msg": parse.group(5)}
        return line_dict
    except AttributeError:
        return None


def extract_modules_greedy(text):
    """贪婪模式：.+ 尽可能多吃字符，从第一个 [ 一直吞到最后一个 ]"""
    return re.findall(r"\[(.+)\]", text)  # 结果：['pay_api] [user_api'] 整段被吞成一坨


def extract_modules_lazy(text):
    """懒惰模式：.+? 尽可能少吃字符，遇到第一个 ] 就收手"""
    return re.findall(r"\[(.+?)\]", text)  # 结果：['pay_api', 'user_api'] 分别提取


if __name__ == "__main__":
    print("--- A 合规用例编号 ---")
    print(extract_case_ids(CASE_TEXT))
    print("--- B 日志行解析 ---")
    for line in LOG_LINES:
        print(parse_line(line))
    print(parse_line("这不是一行日志"))  # 边界：非法行应返回 None 而不是崩溃
    print("--- C 贪婪 vs 懒惰 ---")
    print("贪婪:", extract_modules_greedy(MODULE_TEXT))
    print("懒惰:", extract_modules_lazy(MODULE_TEXT))

    # 1.提取出TC123，使用"TC\d{3}(?!\d)
    # 2.标注字符串的开头和结尾，字符串必须要是这个格式才匹配，如果不加，字符串里面存在这个格式就能匹配，可能已经被污染了，所以去掉后可以解析出来
    # 3.性能好一点，可维护性高
