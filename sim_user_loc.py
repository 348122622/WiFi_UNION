# coding=utf-8
import connect_db_users
import math
import trans_json

def build_dataset_user_loc():
    """
    构造用户地理位置数据集
    结构为{'用户'：{'纬度':'','经度':''},...}
    :return: dataset_user_loc:dict
    """
    data_tuple = connect_db_users.connect_db()
    # 连接数据库
    dataset_user_loc = {}
    for user_info in data_tuple:
        if user_info[0] not in dataset_user_loc:
            dataset_user_loc[user_info[0]] = {}
        dataset_user_loc[user_info[0]]["lat"] = float(user_info[3])
        dataset_user_loc[user_info[0]]["lng"] = float(user_info[4])
    return dataset_user_loc


def sim_rank_euclid(user_mac ,dataset_user_loc):
    """
    基于经纬度的欧式距离计算用户之间的相似度
    :param usermac: str
    :param dataset_user_loc: dict
    :return:
    """
    assert isinstance(user_mac, str)
    assert isinstance(dataset_user_loc, dict)
    sim_rank = []
    for user in dataset_user_loc:
        if user != user_mac:
            lat_distance = pow(dataset_user_loc[user_mac]['lat'] - dataset_user_loc[user]['lat'], 2)
            lng_distance = pow(dataset_user_loc[user_mac]['lng'] - dataset_user_loc[user]['lng'], 2)
            distance = math.sqrt(lat_distance+lng_distance)
            sim = (1/(1+distance), user)
            # 相似度列表结构[(相似度，用户mac),...],降序
            sim_rank.append(sim)
    sim_rank.sort()
    sim_rank.reverse()
    return sim_rank


if __name__ == '__main__':
    try:
        dataset_user_loc = build_dataset_user_loc()
        print (dataset_user_loc)
        print (sim_rank_euclid('70720d07f7e0', dataset_user_loc))
    except Exception as e:
        print ('用户位置相似列表生成失败')
        print (Exception, ':', e)
    else:
        print ('用户位置相似列表生成成功')