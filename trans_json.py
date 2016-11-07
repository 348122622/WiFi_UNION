# coding=utf-8
import json


def data_to_json(data):
    """
    将数据转换为json格式
    :param data: dict/tuple/list/...
    :return: json
    """
    result = json.dumps(data, encoding="UTF-8", ensure_ascii=False, sort_keys=True, indent=4)
    return result

