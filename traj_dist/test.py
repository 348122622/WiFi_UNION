import numpy as np
import pymysql
from DBUtils.PooledDB import PooledDB
import time
import traj_dist.distance as tdist


def conndbWithPool():

    pool = PooledDB(pymysql, 5, host="10.103.31.129", user="nmy", passwd="819819", db="wifi_union", port=3306)  # 5为连接池里的最少连接数

    conn = pool.connection()

    cur = conn.cursor()
    SQL = "SELECT usermac,latitude,longitude FROM wifi_union.appunion_log_detailed_concise where  latitude<>0 group by time order by usermac limit 10;"
    r = cur.execute(SQL)
    r = cur.fetchall()
    cur.close()
    conn.close()

    return r

rs=conndbWithPool()
print(rs)

# for i in rs:
#     if i[0] not in user:
#         user[i[0]]=list([i[1],i[2]])
#     else:
#         user[i[0]]=list(user[i[0]]).append(list([i[1],i[2]]))
        # user[i[0]]=user[i[0]].append[i[1],i[2]]
user = {}
def store_to_dirct(rs):
    new_list = []
    for n in rs:
        if n[0] not in user:
            new_list=[]
        new_list.append(list(map(float, [n[1],n[2]])))
        user[n[0]]=new_list
    return user

