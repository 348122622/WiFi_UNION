# coding=utf-8
import build_cold_start
import trans_pickle
import trans_json
import time


def recommend(user_mac, data_cold_start):
    """
    基于地理位置推荐
    :param user_mac: str
    :param data_cold_start: dict
    :return: dict
    """
    assert isinstance(user_mac, str)
    assert isinstance(data_cold_start, dict)
    # 类型监测
    return data_cold_start[user_mac]


if __name__ == '__main__':
    try:
        data_cold_start = trans_pickle.load('coldStartData')
    except Exception as e:
        print('从本地载入冷启动数据出错')
        print (Exception, ':', e)
    else:
        print ('载入冷启动数据成功')

    result_dict = recommend('70720d07f7e0', data_cold_start)
    print ('基于位置的推荐结果：', trans_json.data_to_json(result_dict))
