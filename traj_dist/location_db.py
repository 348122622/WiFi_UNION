import numpy as np
import pymysql
from DBUtils.PooledDB import PooledDB
import time
import traj_dist.distance as tdist
import math

start = time.clock()

def conndbWithPool():

    pool = PooledDB(pymysql, 5, host="10.103.31.129", user="nmy", passwd="819819", db="wifi_union", port=3306)  # 5为连接池里的最少连接数
    conn = pool.connection()
    cur = conn.cursor()
    SQL = "SELECT usermac,latitude,longitude FROM wifi_union.appunion_log_detailed_concise where  latitude<>0 group by time order by usermac;"
    r = cur.execute(SQL)
    r = cur.fetchall()
    cur.close()
    conn.close()

    return r

def store_to_dirct(rs):
    user = {}
    new_list = []
    for n in rs:
        if n[0] not in user:
            new_list=[]
        new_list.append(list(map(float, [n[1],n[2]])))
        user[n[0]]=new_list
    return user


def computeNearestNeighbor(user,username):
    distances = []
    for instance in user:
        if instance != username:
            distance = tdist.edr(np.array(user[username]), np.array(user[instance]))
            #对豪斯多夫距离取对数加1的倒数
            # distance=1/(math.log10(distance)+1)
            distances.append((instance, distance))
    distances.sort(key=lambda artistTuple: artistTuple[1], reverse=False)
    return distances

rs=conndbWithPool()

user=store_to_dirct(rs)


# print(user)
# traj_A=np.array(user['28faa04f853a'])
# traj_B=np.array(user['C4500620C219'])
#
# dist = tdist.hausdorff(traj_A,traj_B)
# print(dist,math.log10(dist))
#
distances=computeNearestNeighbor(user,'C4500620C219')
print(distances)

end=time.clock()
print ("read: %f s" % (end - start))


