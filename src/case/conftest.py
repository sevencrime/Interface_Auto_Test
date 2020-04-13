#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json
from functools import reduce


from src.util.get_apiData import generate_param

def api_info():
    '''
    读取json文件的数据
    :return: apis, 读取后的dict数据
    '''
    try:
        with open("../api_json/{}.json".format("API_301"), encoding='utf-8') as f:
            apis = json.load(f)
    except IOError as e:
        print(e)
    except json.decoder.JSONDecodeError:
        print("json文件格式有误")

    return apis

@pytest.fixture()
def apis():
    '''
    作为一个fixture, 把数据传递给test测试函数
    :return:
    '''
    return api_info()


def pytest_generate_tests(metafunc):
    if 'data' in metafunc.fixturenames:
        apis = api_info()
        # 自动生成测试数据
        API_KEY_DATA = generate_param().get_api_key_data(apis)
        # 各参数的组合, 匿名函数
        fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
        # 存放所有的参数组合, list
        datalist = []
        for i in fn([i for i in API_KEY_DATA.values()]):
            data = dict(zip([k for k in API_KEY_DATA.keys()], i.split(",")))

            # 处理组合后的参数类型
            for k, v in data.items():
                if not isinstance(data[k], type(API_KEY_DATA[k][0])):

                    if type(API_KEY_DATA[k][0]) == int:
                        try:
                            data[k] = int(data[k])
                        except:
                            data[k] = float(data[k])
                    elif type(API_KEY_DATA[k][0]) == str:
                        data[k] = str(data[k])
                    else:
                        raise TypeError

            datalist.append(data)

        # 参数化数据
        metafunc.parametrize("data", datalist)
