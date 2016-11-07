# coding=utf-8
import pickle


def dump(filename, data):
    """
    将data写入本地pickle文件，文件名为filename
    :param filename:str
    :param data: tuple/dict/...
    :return:
    """
    assert isinstance(filename, str)
    pickle_file = open(filename+'.pkl', 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()


def load(filename):
    """
    读取本地pickle文件的数据
    :param filename: str
    :return: data:tuple/dict/...
    """
    assert isinstance(filename, str)
    pickle_file = open(filename+'.pkl', 'rb')
    data = pickle.load(pickle_file)
    pickle_file.close()
    return data
