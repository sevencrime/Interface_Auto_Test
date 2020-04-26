#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests_toolbelt import MultipartEncoder

from src.util.GlobalMap import GlobalMap


class Post_json:

    gm = GlobalMap()

    def postJson(self, apis, generateData=None, timeout=60):

        if isinstance(apis, dict):
            apis = [apis]

        session = requests.session()
        for api in apis:

            # 处理全局变量
            # str_api = json.dumps(api)
            # if '%' in str_api:
            #     api = json.loads(str_api % globals())

            # 获取接口相关项
            url = api.get('url')
            method = api.get('method')
            c_type = api.get('type')
            headers = api.get('headers')
            cookies = api.get('cookies')
            params = api.get('params')
            data = api.get('data')
            files = api.get('files')
            test_name = api.get('test_name')


            # 特定动作(系统标签)
            _store = api.get('STORE') # 存储变量
            _assert = api.get('ASSERT') # 结果断言

            # 判断整个params是否用到变量
            if "%" in str(params):
                # 处理params参数化数据
                for k in params.keys():
                    # 遍历出具体的value需要参数化
                    if "%" in params[k]:
                        # 遍历全局变量是否有可替换的数据
                        for mapkey, mapvalue in self.gm._map.items():
                            if mapkey in generateData:
                                generateData[mapkey] = mapvalue

                        params[k] = str(generateData)


            # 如果json请求，转换一下数据
            if c_type and c_type == 'json' or headers and 'json' in json.dumps(headers):
                data = json.dumps(data)
            elif c_type and c_type == "form-data":
                # post 的请求方式为: form-data
                data = MultipartEncoder(fields=params)
                headers['Content-Type'] = data.content_type

            import pdb; pdb.set_trace()
            # 根据method发送不同请求
            if not method or method.lower() == 'post': # 有data字段默认使用post方法
                response = session.post(url=url, headers=headers, cookies=cookies, data=data, files=files, timeout=timeout)
            elif not data or method.lower() == 'get': # 没有data字段默认采用get方法
                  response = session.get(url=url, headers=headers, cookies=cookies, params=params, timeout=timeout)
            elif method.lower() == 'delete':
                response = session.delete(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)
            elif method.lower() == 'put':
                response = session.put(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)
            elif method.lower() == 'patch':
                response = session.patch(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)
            elif method.lower() == 'head':
                response = session.head(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)
            else:
                print("不支持当前方法")
            
            # 处理响应
            try:
                # response_text = json.dumps(response.json(), ensure_ascii=False, indent=2)
                response_text = response.json()
            except json.decoder.JSONDecodeError:  # only python3
                try:
                    response_text = response.text
                except UnicodeEncodeError:
                    # print(response.content.decode("utf-8","ignore").replace('\xa9', ''))
                    response_text = response.content
            finally:
                pass

            # 存储中间结果
            if _store:
                for key in _store:
                    try:
                        self.gm.set_map(key, eval(_store[key]))
                    except KeyError:
                        print("接口异常")
                        print("接口返回的数据为 response_text : {}".format(response_text))
                        raise KeyError


            # 处理断言
            status = "PASS"
            if _assert:
                assert_results = []
                for item in _assert:
                    try:
                        # eval() 函数用来执行一个字符串表达式，并返回表达式的值
                        if isinstance(eval(item), dict):
                            try:
                                # 如果是dict, 则对比resp
                                assert all((k in response_text and response_text[k] == v) for k, v in eval(item).items())
                                assert_results.append("PASS: <{}>".format(item))
                            except AssertionError:
                                for value in response_text.values():
                                    if isinstance(value, dict):
                                        assert all((k in value and value[k] == v) for k, v in eval(item).items())
                                        assert_results.append("PASS: <{}>".format(item))
                                    elif isinstance(value, list):
                                        for son_value in value:
                                            if isinstance(son_value, dict):
                                                assert all((k in son_value and son_value[k] == v) for k, v in eval(item).items())
                                                assert_results.append("PASS: <{}>".format(item))
                        else:
                            assert eval(item)
                            assert_results.append("PASS: <{}>".format(item))
                    except AssertionError:
                        assert_results.append("FAIL: <{}>".format(item))
                        status = "FAIL"
                    except Exception as e:
                        # repr() 函数将对象转化为供解释器读取的形式
                        assert_results.append("ERROR: <%s>\n%s" % (item, repr(e)))
                        status = "ERROR"



            # 打印结果
            print("="*80)
            print("正在请求 {} 接口".format(api.get('name')))
            print("用例名称 : {}".format(test_name))
            print("URL : {}".format(url))
            print("headers : {}".format(headers))
            print("data : {}".format((data or params)) )
            print("-"*80)
            print("响应:")
            print(response_text)
            if _assert:
                print("-"*80)
                print("断言:")
                for assert_result in assert_results:
                    print(assert_result)
            print("=" * 80)
            print("\n\n")

            assert status == "PASS"