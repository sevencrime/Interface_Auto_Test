#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from src.util.GlobalMap import GlobalMap
from src.util.post_json import Post_json


class Test_Run:

    gm = GlobalMap()

    def test_run(self, apis, name, phone, age):
        params = {}
        params['name'] = name
        params['phone'] = phone
        params['age'] = age

        print(apis)
        Post_json().postJson(apis=apis, generateData=params)




if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_run.py::Test_Run::test_run"])
