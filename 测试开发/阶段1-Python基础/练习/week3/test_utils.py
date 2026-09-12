def load_config(env="test"):
    """
    输入环境名，返回对应环境配置，默认返回test环境配置
    :param env: 环境名
    :return: 环境配置
    """
    environment = {"test": {"base_url": "http://test.api.com", "timeout": 10},
                   "prod": {"base_url": "http://api.com", "timeout": 5}}
    return environment.get(env, environment["test"])


def count_by_status(results):
    """
    传入状态列表，统计每个状态的个数
    :param results: 状态列表
    :return: 计数字典
    """
    re_dic = {}
    for result in results:
        re_dic[result] = re_dic.get(result, 0) + 1
    return re_dic


def is_success(code):
    """
    传入状态码，判断成功或失败，成功返回True,失败返回False
    :param code:状态码
    :return: bool
    """
    return 200 <= code <= 299


if __name__ == '__main__':
    print(load_config(env="prod"))
    results = ["PASS", "FAIL", "PASS", "SKIP", "FAIL"]
    print(count_by_status(results))
    print(is_success(300))
    print(is_success(299))
    print(is_success(200))
