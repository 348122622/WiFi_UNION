# coding=utf-8
import connect_db_users
import build_stores_dataset
import trans_json
import trans_pickle
import math
import time


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


def sim_euclid(dataset_user_loc, user_mac, store_data, store_name):
    """
    计算用户和商户经纬度之间的欧几里得距离,得相似度
    :param dataset_user_loc:dict
    :param user_mac:str
    :param store_data:dict
    :param store_name:str
    :return:float
    """
    assert isinstance(dataset_user_loc, dict)
    assert isinstance(user_mac, str)
    assert isinstance(store_data, dict)
    assert isinstance(store_name, unicode)
    # 商户名称为中文，类型为unicode
    # 类型监测
    lat_distance = pow(float(dataset_user_loc[user_mac]['lat']) - float(store_data[store_name]['lat']), 2)
    lng_distance = pow(float(dataset_user_loc[user_mac]['lng']) - float(store_data[store_name]['lng']), 2)
    distance_euclid = math.sqrt(lat_distance + lng_distance)
    sim = 1 / (1 + distance_euclid)
    return sim


def build_data_cold_start(dataset_user_loc, store_data, n=10, similarity=sim_euclid):
    """
    对用户地理位置数据集中的每个数据进行推荐，构造冷启动数据
    结构为双重嵌套字典{‘a用户mac’:{'商户1':{'参数1'：‘参数值1’，....}......}.......}
    :param dataset_user_loc: dict
    :param store_data: dict
    :param n: int
    :param similarity: func
    :return: dict
    """
    data_cold_start = {}
    for user_mac in dataset_user_loc:
        if user_mac not in data_cold_start:
            data_cold_start[user_mac] = {}
        sim_rank = [(store_name, similarity(dataset_user_loc, user_mac, store_data, store_name)) for store_name in
                    store_data]
        sim_rank.sort()
        sim_rank.reverse()
        sim_rank = sim_rank[0:n]
        # print sim_rank
        # # 查看相似度列表
        for i in sim_rank:
            # sim_rank数据结构为list  [(a商户名字，相似度值),.....]
            data_cold_start[user_mac][i[0]] = store_data[i[0]]
    return data_cold_start


if __name__ == '__main__':
    start_load_users = time.clock()

    dataset_user_loc = build_dataset_user_loc()
    # 构建用户位置数据集{'用户'：{'纬度':'','经度':''},...}
    # print dataset_user_loc
    final_load_users = time.clock()
    print '读取用户信息用时：%f s' % (final_load_users - start_load_users)

    start_load_stores = time.clock()

    store_data = build_stores_dataset.build_dataset()
    # 构造商户数据集,lat和lng的下标分别为2和3{‘a商户名字’:{'address':'','lat':'','lng':'',...}..........}
    # for store in store_data:
    #     print store, store_data[store]['lat'],  store_data[store]['lng']
    # # 查看商户经纬度信息

    final_load_stores = time.clock()
    print "读取商户信息用时： %f s" % (final_load_stores - start_load_stores)

    start_cold_start = time.clock()

    data_cold_start = build_data_cold_start(dataset_user_loc, store_data)
    # # 构建冷启动数据集
    # print trans_json.data_to_json(data_cold_start)
    final_cold_start = time.clock()
    print '构建冷启动数据集用时：%f s' % (final_cold_start - start_cold_start)

    trans_pickle.dump('coldStartData', data_cold_start)
