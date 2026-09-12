test_results = []
execution_count = 0


def record_result(status):
    """
    传入执行结果，将执行结果加入执行结果列表，并统计执行数量
    :param status: 执行结果
    :return: None
    """
    global execution_count
    test_results.append(status)

    execution_count += 1


def reset():
    """
    重置执行结果列表为[]，执行数量为0
    :return: None
    """
    global execution_count
    global test_results

    test_results = []
    execution_count = 0


def add_tag_buggy(tag, tags=[]):
    """
    将标签加入标签列表，返回标签列表
    :param tag: 标签
    :param tags: 标签列表
    :return: tags
    """
    tags.append(tag)
    return tags


def add_tag_fixed(tag, tags=None):
    """
    将标签加入标签列表，返回标签列表
    :param tag: 标签
    :param tags: 标签列表
    :return: 标签列表
    """
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


record_result("PASS")
record_result("FAIL")
record_result("PASS")

print("结果列表:", test_results)
print("执行次数:", execution_count)

reset()
print(f"重置后: 列表={test_results}, 计数={execution_count}")

record_result("SKIP")
print(f"重新记录后执行次数: {execution_count}")
tags = add_tag_buggy("smoke")
print(tags)

tags = add_tag_buggy("regression")
print(tags)

tags = add_tag_fixed("smoke")
print(tags)
tags = add_tag_fixed("regression")
print(tags)
