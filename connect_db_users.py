# coding=utf-8
import pymysql
from DBUtils.PooledDB import PooledDB


def connect_db():
    """
    连接数据库，读取用户数据，结构为(('000ce7d31aa6', 6, 0, '0', '0'), ('00aefadd2b26', 6, 0, '0', '0'), ('020000000000', 6, 0,
    '0', '0'),('0c1daf66152c', 6, 0, '22.847936', '113.251772'), ('0cd6bd69330b', 6, 0, '0', '0'),...)
    :return: tuple
    """

    pool = PooledDB(pymysql, 5, host="10.103.31.129", user="admin", passwd="819819", db="wifi_union", port=3306)
    # 5为连接池里的最少连接数
    conn = pool.connection()
    cur = conn.cursor()
    # sql = "SELECT usermac as um, weekday(date) as dc, hour(time) as tc, latitude as lat, longitude as lng FROM " \
    #       "wifi_union.appunion_log_detailed_concise where id < 100  group by um,dc,tc;"
    #查询结果的时间、地点、用户已经分组，并过滤掉用户只经过一次的地点
    sql="SELECT usermac as um, weekday(date) as dc, hour(time) as tc, latitude as lat, longitude as lng " \
        "from wifi_union.appunion_log_detailed_filtered as table1 " \
        "LEFT JOIN (SELECT area,count(*) as fre FROM wifi_union.appunion_log_detailed_filtered group by area having fre>1) as table2" \
        " ON table1.area=table2.area" \
        " where  fre is not null"

    cur.execute(sql)
    data_tuple = cur.fetchall()
    cur.close()
    conn.close()
    return data_tuple

if __name__ == '__main__':
    try:
        connect_db()
    except Exception as e:
        print('连接数据库失败')
        print (Exception, ":", e)
    else:
        print ('连接数据库成功')
