def send_request(url, method="GET", timeout=10):
    """
    打印请求信息
    :param url: 接口路径
    :param method: 请求方法
    :param timeout: 超时时间
    :return: None
    """

    print(f"发送 {method} 请求 → {url}（超时 {timeout}s）")


def log_results(*results):
    """
    打印执行结果
    :param results: 执行结果列表
    :return: None
    """
    print(f"共收到 {len(results)} 条结果")
    for i in range(len(results)):
        print(f"第 {i + 1} 条: {results[i]}")


def build_url(base, **params):
    """
    打印完整查询链接

    :param base: url
    :param params: 查询入参
    :return: None
    """
    if params:
        url = base + "?" + "&".join(f"{key}={value}" for key, value in params.items())
    else:
        url = base
    print(url)


send_request("http://api.example.com/login")  # 全默认
send_request("http://api.example.com/order", method="POST", timeout=30)  # 关键字覆盖
log_results("PASS", "FAIL", "PASS")
log_results("SKIP")
build_url("http://api.example.com/users", page=2, size=10)
build_url("http://api.example.com/health")  # 无参数边界
