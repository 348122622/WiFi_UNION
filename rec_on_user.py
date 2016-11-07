# coding=utf-8
import sim_user_loc
import sim_user_time
import trans_json
import trans_pickle


def sim_rank(sim_loc_rank, sim_time_rank, n=5):
    """
    按自定权重合并用户时间和位置相似度列表
    :param sim_loc_rank: list
    :param sim_time_rank: list
    :return: list
    """
    assert isinstance(sim_loc_rank, list)
    assert isinstance(sim_time_rank, list)
    sim_rank =[]
    for sim_loc in sim_loc_rank:
        for sim_time in sim_time_rank:
            if sim_loc[1] == sim_time[1]:
                sim = (float(sim_loc[0])+float(sim_time[0])) / 2
                # 自定义时间，位置相似度权重
                sim_rank.append((sim, sim_loc[1]))
    sim_rank.sort()
    sim_rank.reverse()
    return sim_rank[0:n]


def recommend(user_mac, filename_cold_start, sim_rank):
    """
    基于用户推荐
    :param user_mac: str
    :param filename_cold_start:str
    :param sim_rank: list
    :return: dict
    """
    assert isinstance(user_mac, str)
    assert isinstance(filename_cold_start, str)
    assert isinstance(sim_rank, list)
    data_cold_start = trans_pickle.load(filename_cold_start)
    result = {}
    for user in sim_rank:
        for store in data_cold_start[user[1]]:
            if store not in result:
                result[store] = data_cold_start[user[1]][store]
    return result


if __name__ == '__main__':
    dataset_user_time = sim_user_time.build_dataset_user_time()
    sim_time_rank = sim_user_time.sim_rank_euclid('70720d07f7e0', dataset_user_time)
    print sim_time_rank
    dataset_user_loc = sim_user_loc.build_dataset_user_loc()
    sim_loc_rank = sim_user_loc.sim_rank_euclid('70720d07f7e0', dataset_user_loc)
    print sim_loc_rank
    print sim_rank(sim_loc_rank, sim_time_rank)
    print trans_json.data_to_json(recommend('70720d07f7e0', 'coldStartData', sim_rank(sim_loc_rank, sim_time_rank)))
