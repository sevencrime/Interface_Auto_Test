#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import json
from functools import reduce


from src.util.get_apiData import generate_param

def api_info():
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
    return api_info()

fn = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)

def pytest_generate_tests(metafunc):
    print("钩子钩子")
    if 'name' in metafunc.fixturenames:
        apis = api_info()
        API_KEY_DATA = generate_param().get_api_key_data(apis)

        import pdb; pdb.set_trace()


        import pdb; pdb.set_trace()
        for k, v in API_KEY_DATA.items():
            metafunc.parametrize(k, v)
