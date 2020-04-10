#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, io
# 改变标准输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
from requests_toolbelt import MultipartEncoder
import requests
import json
import time
from commond.GlobalMap import GlobalMap


class request_case:

	gm = GlobalMap()

	def login(self, url):
		m = MultipartEncoder(fields={'QueryString': '{"account":"3001331112","password":"wjxpg4","branch_no":"","account_type":"8","MF":201,"op_station":"ZctPcY8BCaT6tCmxYYPc6TwcnPKCTxpQ","op_entrust_way":"A","language_type":"1"}'})
		resp = requests.post(url, data=m, headers={'Content-Type' : m.content_type})

		try:
			assert resp.json()['error_info'].strip() == "ok"
			print("\n登录接口返回的数据为 : {}".format(resp.json()))
			return resp.json()
		except AssertionError:
			raise AssertionError

	def _replace_all(self, body):
		return body.replace("{{session_no}}", (self.gm.get_value("session_no") or "0")).replace("{{thread_id}}", 
			self.gm.get_value("thread_id")).replace("{{entrust_no}}", (self.gm.get_value("entrust_no") or "0"))


	def dataProcessing(self, casedata):
		# print(casedata)

		rowNum = casedata['rowNum']

		# 解析预置条件
		Preconditionslist = (casedata['Preconditions'] or "").split("MF=")
		if Preconditionslist.__len__() > 1:
			MFlist = Preconditionslist[1].split(",")
			for MF in MFlist:
				pass
				# 取出MF对应的参数, 然后调用request
				# self.request()

		method = casedata['method'].strip()		#从excel读取method
		url = casedata['URL'].strip()		#从excel中读取url
		expected = casedata['Expected_Response']		#从excel中读取期望结果

		if rowNum in [2, 63, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 82, 83]:
			# self.session_no = str(self.login())
			loginres = self.login(url)
			self.gm.set_value(session_no=str(loginres['data']['session_no']))
			self.gm.set_value(thread_id=str(loginres['data']['thread_id']))

		if (casedata['body'] or "") != "":
			body = self._replace_all(casedata['body'])
			m = MultipartEncoder(fields={'QueryString': body})
		else:
			body = ""
			m = ""

		#从excel中获取headers，判断是否为空
		if casedata['headers'] != "":
			headers = json.loads(casedata["headers"])
			if m != "":
				headers['Content-Type'] = m.content_type
		else:
			headers = ""

		print("\n***************正在执行第 %s 条用例******************" %(rowNum-1))
		print("用例标题 : {}".format(casedata['name']))
		print("请求方式: {} ".format(method))
		print("请求接口: {}".format(url))
		print("请求头 : {}".format(headers))
		print("请求参数: {} ".format(body))

		return self.request(method, url, m, headers)



	def request(self, method, url, data, headers):
		# s = requests.session()

		try:
			response = requests.request(method=method,url=url,data=data, headers=headers)
			print("status_code : {}".format(response.status_code))
			print("响应时间为 : {}".format(response.elapsed.total_seconds()))
			print("响应数据为 : {}".format(response.json()))
			assert response.status_code == 200
			# if response.json()['error_info'] == '由于长时间未操作或其他原因，为确保您的交易安全，请重新登录!':
			# 	import pdb; pdb.set_trace()

			return response.json(), response.elapsed.total_seconds()
		except Exception as e:
			print("异常信息为 : {}".format(e))
			return "ERROR", "ERROR"



	def postJson(path, timeout=60):
	    try:
	        with open(path, encoding='utf-8') as f:
	            apis = json.load(f)
	    except IOError as e:
	        print(e)

	    except json.decoder.JSONDecodeError:
	        print("json文件格式有误")
	        
	    if isinstance(apis, dict):
	        apis=[apis]

	    session = requests.session()
	    for api in apis:

	        # 处理全局变量
	        str_api = json.dumps(api)
	        if '%' in str_api:
	            api = json.loads(str_api % globals())

	        # 获取接口相关项
	        url = api.get('url')
	        method = api.get('method')
	        type = api.get('type')
	        headers = api.get('headers')
	        cookies = api.get('cookies')
	        params = api.get('params')
	        data = api.get('data')
	        files = api.get('files')

	        # 特定动作(系统标签)
	        _sign = api.get('SIGN')  # 对数据进行签名
	        _store = api.get('STORE') # 存储变量
	        _assert = api.get('ASSERT') # 结果断言
	        
	        # 处理签名
	        if _sign:
	        	data = makeSign(data)

	        # 如果json请求，转换一下数据
	        if type and type == 'json' or headers and 'json' in json.dumps(headers):
	            data = json.dumps(data)

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




if __name__ == '__main__':
	# casedata = {'rowNum': 2, 'case': 1.0, 'module': 'ayers新网关', 'Submodule': '委托下单', 'level': 'high', 'test_type': '接口测试', 'name': '登录后, 必填参数正常入参, 可以成功下单', 'Preconditions': '', 'URL': 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx', 'method': 'POST', 'headers': '{\n    "Content-Type":"application/x-www-form-urlencoded"\n    "User-Agent":"Openwave"\n    "Content-Language":"en-US"\n}', 'body': '{\n    "MF": 301,\n    "fund_account": "3001331112",\n    "exchange_type": "K",\n    "stock_account": "3001331112",\n    "stock_code": "00008",\n    "entrust_amount": 10000,\t\n    "entrust_price": 0.047,\n    "entrust_bs": "B",\n    "entrust_prop": "e",\n    "op_station": "isX5db4FstXj2MdW3weZGcpAktjHG4nM",\n    "session_no": {{session_no}}\n}', 'Expected_Response': '{"error_no":0,"error_info":"ok","error_info_ansi":"","data":{"entrust_no":"11190","order_status":"WA"}}', '测试轮次': '', '执行人': '', '测试结果': '', '备注': ''}
	# request_case().requests(casedata)

	m = MultipartEncoder(fields={'QueryString' : "{'MF': 301, 'fund_account': '3001331112', 'exchange_type': 'K', 'stock_account': '3001331112', 'stock_code': '00008', 'entrust_amount': 10000, 'entrust_price': 0.047, 'entrust_bs': 'B', 'entrust_prop': 'e', 'op_station': 'isX5db4FstXj2MdW3weZGcpAktjHG4nM', 'session_no': 0}"})
	print(m.content_type)
	# url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'
	# headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Openwave', 'Content-Language': 'en-US'}
	# response=requests.post(url,data=m, headers={'Content-Type': m.content_type})
	# print(response.json())

	# resp = request_case().login()
	# print(resp)