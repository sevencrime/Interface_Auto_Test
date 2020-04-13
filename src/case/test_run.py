#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from src.util.GlobalMap import GlobalMap
from src.util.post_json import Post_json


class Test_Run:

    gm = GlobalMap()

    def test_run(self, apis, data):
        print(data)
        Post_json().postJson(apis=apis, generateData=data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_run.py::Test_Run::test_run", "--pdb"])
