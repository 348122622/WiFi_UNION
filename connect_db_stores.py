# coding=utf-8
import pymysql
from DBUtils.PooledDB import PooledDB


def connect_db():
    """
    从数据库读取商户数据
    返回数据结构((商户名字，商户类型，环境评分，地址，纬度，经度，平均消费，评论数，评论星级，电话，环境评分),...)
    :return: tuple
    """
    pool = PooledDB(pymysql, 5, host="10.103.31.129", user="admin", passwd="819819", db="wifi_union", port=3306,
                    charset="utf8")
    # 5为连接池里的最少连接数
    conn = pool.connection()
    cur = conn.cursor()
    sql = "SELECT name, type, score_service, address, lat, lng, average_consumption, comment_count, comment_star, " \
          "phone_number, score_environment FROM dianping WHERE id < 100;"
    cur.execute(sql)
    stores_data_tuple = cur.fetchall()
    cur.close()
    conn.close()
    return stores_data_tuple


if __name__ == '__main__':
    try:
        connect_db()
    except Exception as e:
        print('连接数据库失败')
        print (Exception, ":", e)
    else:
        print ('连接数据库成功')