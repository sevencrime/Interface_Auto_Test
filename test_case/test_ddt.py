#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import pytest
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("Interface_Auto_Test\\") + len("Interface_Auto_Test\\")]
import sys
sys.path.append(rootPath)
from commond.read_xls import Read_xls
from commond.get_apiData import generate_param
from request_case import request_case
import allure
import json




class Test_ddt:
	# 获取excel用例
	path = rootPath + r'docs/data.xlsx'
	orderList = Read_xls(path, u"委托下单").read()
	cancelOrder = Read_xls(path, u"委托撤单").read()

	# 委托下单
	@pytest.mark.parametrize("testdata", orderList)
	def test_interface(self, testdata):
		# print(testdata)

		response, resp_time = request_case().dataProcessing(testdata)
		# 写入数据
		# self.exl.write(testdata, response, resp_time)

	def test_read_jsonfile(self):
		# 读取json文件
		with open("../test_file/test.json",'r') as load_f:
			load_dict = json.load(load_f)
			print(load_dict)

		API_KEY_DATA = generate_param().get_api_key_data(load_dict)
		print(API_KEY_DATA)



if __name__ == '__main__':
	pytest.main(["-v", "-s", "test_ddt.py::Test_ddt::test_read_jsonfile"])

	# 15033330000,psw=abcd1234  证券: 3001331110,psw=jxy7ke  期货: 800333216, psw=123456
	#
	# 15033331111,psw=abcd1234  证券: 3001331112,psw=wjxpg4  期货: 3001333212, psw=123456
