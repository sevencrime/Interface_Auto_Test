#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from src.util.post_json import Post_json
import json

class Test_Run:

    def test_run(self, apis, data):
        print(json.dumps(data))

        if isinstance(apis, list):
            for api in apis:
                Post_json().postJson(apis=api, generateData=data)
        else:
            Post_json().postJson(apis=apis, generateData=data)


if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_run.py::Test_Run", "--pdb"])
