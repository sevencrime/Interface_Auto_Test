#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_toolbelt import MultipartEncoder
import requests
import json

from commond.GlobalMap import GlobalMap


class request_case:

	gm = GlobalMap()

	def login(self):
		url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'
		m = MultipartEncoder(fields={'QueryString': '{"account":"3001331112","password":"wjxpg4","branch_no":"","account_type":"8","MF":201,"op_station":"ZctPcY8BCaT6tCmxYYPc6TwcnPKCTxpQ","op_entrust_way":"A","language_type":"1"}'})
		resp = requests.post(url, data=m, headers={'Content-Type' : m.content_type})

		try:
			assert resp.json()['error_info'].strip() == "ok"
			return resp.json()['data']['session_no']
		except AssertionError:
			raise AssertionError

	def requests(self, casedata):

		print(casedata)

		rowNum = casedata['rowNum']
		if rowNum % 10 == 0 or rowNum == 2:
			# self.session_no = str(self.login())
			self.gm.set_value(session_no=str(self.login()))

		method = casedata['method']		#从excel读取method
		url = casedata['URL']		#从excel中读取url
		expected = casedata['Expected_Response']		#从excel中读取期望结果

		if casedata['body'] != "":

			body = casedata['body'].replace("{{session_no}}", (self.gm.get_value("session_no") or "0"))
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

		print("***************正在执行第 %s 条用例******************" %(rowNum-1))
		print("用例标题 : {}".format(casedata['name']))
		print("请求方式: {} ".format(method))
		print("请求接口: {}".format(url))
		print("请求头 : {}".format(headers))
		print("请求参数: {} ".format(body))
		s = requests.session()
		# proxies = self.get_random_ip(ip_list)
		# print("proxies 代理为 {}".format(proxies))

		# if method == "POST" or method == "post":
		# 	response = requests.post(url=url,data=m, headers={'Content-Type': m.content_type})

		try:
			response = s.request(method=method,url=url,data=m, headers=headers)
			print("status_code : {}".format(response.status_code))
			print("响应数据为 : {}".format(response.json()))
			assert response.status_code == 200
			return response.json()
		except Exception as e:
			print("异常信息为 : {}".format(e))
			return "ERROR"


if __name__ == '__main__':
	# casedata = {'rowNum': 2, 'case': 1.0, 'module': 'ayers新网关', 'Submodule': '委托下单', 'level': 'high', 'test_type': '接口测试', 'name': '登录后, 必填参数正常入参, 可以成功下单', 'Preconditions': '', 'URL': 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx', 'method': 'POST', 'headers': '{\n    "Content-Type":"application/x-www-form-urlencoded"\n    "User-Agent":"Openwave"\n    "Content-Language":"en-US"\n}', 'body': '{\n    "MF": 301,\n    "fund_account": "3001331112",\n    "exchange_type": "K",\n    "stock_account": "3001331112",\n    "stock_code": "00008",\n    "entrust_amount": 10000,\t\n    "entrust_price": 0.047,\n    "entrust_bs": "B",\n    "entrust_prop": "e",\n    "op_station": "isX5db4FstXj2MdW3weZGcpAktjHG4nM",\n    "session_no": {{session_no}}\n}', 'Expected_Response': '{"error_no":0,"error_info":"ok","error_info_ansi":"","data":{"entrust_no":"11190","order_status":"WA"}}', '测试轮次': '', '执行人': '', '测试结果': '', '备注': ''}
	# request_case().requests(casedata)

	# m = MultipartEncoder(fields={'QueryString' : "{'MF': 301, 'fund_account': '3001331112', 'exchange_type': 'K', 'stock_account': '3001331112', 'stock_code': '00008', 'entrust_amount': 10000, 'entrust_price': 0.047, 'entrust_bs': 'B', 'entrust_prop': 'e', 'op_station': 'isX5db4FstXj2MdW3weZGcpAktjHG4nM', 'session_no': 0}"})
	#
	# url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'
	# headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Openwave', 'Content-Language': 'en-US'}
	# response=requests.post(url,data=m, headers={'Content-Type': m.content_type})
	# print(response.json())

	resp = request_case().login()
	print(resp)