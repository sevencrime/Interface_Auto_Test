#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import xlrd
import sys
import os
from xlutils.copy import copy

import xlwt

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("Interface_Auto_Test\\") + len("Interface_Auto_Test\\")]
sys.path.append(rootPath)

class Read_xls:

	def __init__(self, path):
		self.path = path
		# 打开文件，获取excel文件的workbook（工作簿）对象
		self.workbook = xlrd.open_workbook(self.path, formatting_info=True)
		self.wb = copy(self.workbook)

	def read(self):

		# print(path)
		# 打开excel文件,open_workbook(path),path为excel所在的路径
		# 打开excel表,这里表示打开第一张表
		table = self.workbook.sheets()[0]

		nrows = table.nrows		# 获取excel的行数
		# print(nrows)
		ncols = table.ncols		#获取excel的列数
		# print(ncols)
		keys = table.row_values(0)		#获取第一行的值
		# print(keys)

		resp = []		#创建一个list，用于存放

		x = 1
		for i in range(nrows-1):
			s = {}
			# print(i)
			s['rowNum'] = i+2 	#加入用例的行数，用户后面写入数据
			values = table.row_values(x)
			# print(values)
			for j in range(ncols):
				# print('j=',j)
				s[keys[j]] = values[j]
			# print(s)
			resp.append(s)
			x += 1

		return resp

	def write(self, testdata, resp):


		# sheet = wb.get_sheet(0)
		# 通过sheet名获取sheet对象
		sheet = self.wb.get_sheet(0)

		style = xlwt.XFStyle()
		# 设置font字体
		font = xlwt.Font()
		alignment = xlwt.Alignment()
		font.name = '宋体'	#字体样式
		font.bold = True	#粗体
		alignment.horz = 0x01
		alignment.vert = 0x00
		alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行
		style.alignment = alignment

		# 写入预期结果, 下标从0 开始算
		sheet.write(testdata['rowNum']-1, 11, str(resp), style)

		self.wb.save(rootPath + r'docs/data_copy.xls')


	# 转换成json文件, 供postman使用
	def get_dict(self, resp):
		list1 = []
		for res in resp:
			# 转换body
			body = res['body'].replace(r"\n", "").replace(" ", "").replace(r'"', r'\"')
			# print(body)

			dict1 = {
				"name": res['name'],
				"event": [
					{
						"listen": "test",
						"script": {
							"id": "ebcbfafb-e5a1-479a-ad0d-afbcf2501538",
							"exec": [
								"pm.test(\"Status code is 200\", function () {",
								"    pm.response.to.have.status(200);",
								"});"
							],
							"type": "text/javascript"
						}
					},
				],
				"request": {
					"method": res['method'],
					"header": [
						{
							"key": "Content-Type",
							"type": "text",
							"value": "application/x-www-form-urlencoded"
						},
						{
							"key": "User-Agent",
							"type": "text",
							"value": "Openwave"
						},
						{
							"key": "Content-Language",
							"type": "text",
							"value": "en-US"
						}
					],
					"body": {
						"mode": "formdata",
						"formdata": [
							{
								"key": "QueryString",
								"value": res['body'],
								"type": "text"
							}
						]
					},
					"url": {
						"raw": "http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx",
						"protocol": "http",
						"host": [
							"trade-route-develop",
							"ntdev",
							"be"
						],
						"port": "8080",
						"path": [
							"GXSocket",
							"NewGateWay.aspx"
						]
					}
				},
				"response": []
			}

			list1.append(dict1)

		# print(list1)

		head_dict = {
			"info": {
				"_postman_id": "bba5b37d-f409-463b-87ff-2bda3e7f839b",
				"name": "sssss",
				"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
			},
			"protocolProfileBehavior": {}
		}
		head_dict['item'] = list1
		# print(head_dict)
		import json
		print(json.dumps(head_dict, ensure_ascii=False))




if __name__ == "__main__":
	# path = 'E:/郑某人/Python_Demo/Interface_Test_Frame/data/data.xls'
	curPath = os.path.abspath(os.path.dirname(__file__))
	rootPath = curPath[:curPath.find("Interface_Auto_Test\\") + len("Interface_Auto_Test\\")]
	path = rootPath+r'docs/data_copy.xls'
	reads = Read_xls(path)
	reads.write({"rowNum" : 3}, "2222222")


