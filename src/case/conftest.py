#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json
from functools import reduce

from src.util.GlobalMap import GlobalMap
from src.util.get_apiData import generate_param


gm = GlobalMap()

def api_info():
    '''
    读取json文件的数据
    :return: apis, 读取后的dict数据
    '''
    try:
        with open("../api_json/{}.json".format("统一认证-注册"), encoding='utf-8') as f:
            apis = json.load(f)
    except IOError as e:
        print(e)
    except json.decoder.JSONDecodeError:
        print("json文件格式有误")

    return apis

@pytest.fixture()
def apis():
    '''
    作为一个fixture, 把数据传递给test测试 函数
    :return:
    '''
    yield api_info()
    # 遍历出_map的key, 再依次删除
    for key in [m for m in gm._map.keys()]:
        gm.del_map(key)

def pytest_generate_tests(metafunc):
    apis = api_info()
    # fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
    if 'data' in metafunc.fixturenames and isinstance(apis, dict):
        if apis.get("body"):
            # 自动生成测试数据
            # API_KEY_DATA, delparamlist = generate_param().get_api_key_data(apis)
            datalist = generate_param().get_api_key_data(apis)
            if apis.get("data"):
                datalist.append(apis.get("data"))
            # 参数化数据
            metafunc.parametrize("data", datalist)
        else:
            metafunc.parametrize("data", apis.get("data"))

    elif 'data' in metafunc.fixturenames and isinstance(apis, list):
        for api in apis:
            if api.get("body"):
                # API_KEY_DATA, delparamlist = generate_param().get_api_key_data(api)
                datalist = generate_param().get_api_key_data(api)
                if api.get("data"):
                    datalist.append(api.get("data"))
                # 参数化数据
                metafunc.parametrize("data", datalist)
