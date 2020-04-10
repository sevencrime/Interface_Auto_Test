#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from requests_toolbelt import MultipartEncoder

class Post_json:

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


            # 特定动作(系统标签)
            _store = api.get('STORE') # 存储变量
            _assert = api.get('ASSERT') # 结果断言

            if "%" in str(params):
                # 处理params参数化数据
                for k in params.keys():
                    params[k] = str(generateData)


            # 如果json请求，转换一下数据
            if c_type and c_type == 'json' or headers and 'json' in json.dumps(headers):
                data = json.dumps(data)
            if c_type and c_type == "form-data":
                # post 的请求方式为: form-data
                data = MultipartEncoder(fields=params)
                headers['Content-Type'] = data.content_type


            # 根据method发送不同请求
            if not method or method.lower() == 'post': # 有data字段默认使用post方法
                response = session.post(url=url, headers=headers, cookies=cookies, params=params, data=data, files=files, timeout=timeout)  
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
            
            # 存储中间结果
            if _store:
                for key in _store:
                    globals()[key]=eval(_store[key])
            
            # 处理响应
            try:
                response_text = json.dumps(response.json(), ensure_ascii=False, indent=2)
            except json.decoder.JSONDecodeError:  # only python3
                try:
                    response_text = response.text
                except UnicodeEncodeError:
                    # print(response.content.decode("utf-8","ignore").replace('\xa9', ''))
                    response_text = response.content
            finally:
                pass

            # 处理断言
            status = "PASS"
            if _assert:
                assert_results = []
                for item in _assert:
                    try:
                        assert eval(item)
                        assert_results.append("PASS: <%s>" % item)
                    except AssertionError:
                        assert_results.append("FAIL: <%s>" % item)
                        status = "FAIL"
                    except Exception as e:
                        assert_results.append("ERROR: <%s>\n%s" % (item, repr(e)))
                        status = "ERROR"
            
            # 打印结果
            print("="*80)
            print("请求:")
            print("Url: %s\nHeaders: %s\nData: %s" % (url, headers, data if isinstance(data, str) else json.dumps(data)))
            print("-"*80)
            print("响应:")
            print(response_text)
            if _assert:
                print("-"*80)
                print("断言:")
                for assert_result in assert_results:
                    print(assert_result)


