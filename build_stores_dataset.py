# coding=utf-8
import connect_db_stores
import trans_json
import trans_pickle
import time


def build_dataset():
    """
    输入商户嵌套元祖数据集
    构造商户数据集{'商户名字'：{'商户类型':''，'环境评分':''，'地址':''，'纬度':''，'经度':''，'平均消费':''，'评论数':''，'评论星级':''，
    '电话':''，'环境评分':''},...}
    (字典是无序的!)
    :return:stores_data:dict
    """
    stores_data_tuple = connect_db_stores.connect_db()
    # 连接数据库
    stores_data = {}
    for store in stores_data_tuple:
        if store[0] not in stores_data:
            # store[0]是商户的name属性值
            stores_data[store[0]] = {}
        stores_data[store[0]]['type'] = store[1]
        stores_data[store[0]]['score_service'] = store[2]
        stores_data[store[0]]['address'] = store[3]
        stores_data[store[0]]['lat'] = float(store[4])
        stores_data[store[0]]['lng'] = float(store[5])
        # 经纬度转换为float类型
        stores_data[store[0]]['average_consumption'] = store[6]
        stores_data[store[0]]['comment_count'] = store[7]
        stores_data[store[0]]['comment_star'] = store[8]
        stores_data[store[0]]['phone_number'] = store[9]
        stores_data[store[0]]['score_environment'] = store[10]
    return stores_data


if __name__ == '__main__':
    try:
        start = time.clock()
        stores_dataset = build_dataset()
        final = time.clock()
    except Exception as e:
        print('构建商户数据集失败')
        print(Exception, ':', e)
    else:
        print('构建商户数据集成功，用时: %f s' % (final - start))