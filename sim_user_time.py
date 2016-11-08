# coding=utf-8
import connect_db_users
import math


def build_dataset_user_time():
    """
    构造用户登录时间数据集
    结构为{'70720d07f7e0': {'2_4': 0.0, '1_6': 0.0, '1_5': 0.0, '1_4': 0.0, '1_3': 0.0,...},....}
    :return: dataset_user_time:dict
    """
    data_tuple = connect_db_users.connect_db()
    dataset_user_time = {}
    for user_info in data_tuple:
        if user_info[0] not in dataset_user_time:
            dataset_user_time[user_info[0]] = {}
            for weekday in range(7):
                for hour_time in range(24):
                    dataset_user_time[user_info[0]][str(hour_time) + '_' + str(weekday)] = float(0)
        dataset_user_time[user_info[0]][str(user_info[2]) + '_' + str(user_info[1])] = 1.0
    return dataset_user_time


def sim_rank_euclid(user_mac, dataset_user_time):
    """
    生成用户时间相似度列表
    :param user_mac: str
    :param dataset_user_time:dict
    :return:
    """
    sim_rank = []
    for user in dataset_user_time:
        if user != user_mac:
            distance = 0.0
            for time in dataset_user_time[user]:
                hour_distance = pow(float(dataset_user_time[user_mac][time])-float(dataset_user_time[user][time]), 2)
                distance += hour_distance
            sim = (1 / (1 + math.sqrt(distance)), user)
            # 相似度列表结构[(相似度，用户mac),...]，降序
            sim_rank.append(sim)
    sim_rank.sort()
    sim_rank.reverse()
    return sim_rank


if __name__ == '__main__':
    try:
        dataset_user_time = build_dataset_user_time()
        print (dataset_user_time)
        print (sim_rank_euclid('70720d07f7e0', dataset_user_time))
    except Exception as e:
        print ('用户时间相似度列表生成失败')
        print (Exception, ':', e)
    else:
        print ('用户时间相似度列表生成成功')


