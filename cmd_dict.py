#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_toolbelt import MultipartEncoder
from commond.read_xls import Read_xls
import os

old_url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/Handle.aspx'
news_url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'

def login(url):
    m = MultipartEncoder(fields={'QueryString': '{"account":"3001331112","password":"abcd1234","branch_no":"","account_type":"8","MF":201,"op_station":"ZctPcY8BCaT6tCmxYYPc6TwcnPKCTxpQ","op_entrust_way":"A","language_type":"1"}'})
    resp = requests.post(url, data=m, headers={'Content-Type' : m.content_type})

    try:
        assert resp.json()['error_info'].strip() == "ok"
        # print("\n登录接口返回的数据为 : {}".format(resp.json()))
        return resp.json()
    except AssertionError:
        raise AssertionError


def requets(old_data, new_data):

    # m = MultipartEncoder(fields={'QueryString' : "{'MF': 301, 'fund_account': '3001331112', 'exchange_type': 'K', 'stock_account': '3001331112', 'stock_code': '00008', 'entrust_amount': 10000, 'entrust_price': 0.047, 'entrust_bs': 'B', 'entrust_prop': 'e', 'op_station': 'isX5db4FstXj2MdW3weZGcpAktjHG4nM', 'session_no': 0}"})
    old_m = MultipartEncoder(fields={'QueryString' : old_data})
    new_m = MultipartEncoder(fields={'QueryString' : new_data})
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Openwave', 'Content-Language': 'en-US'}

    old_resp = requests.post(old_url, data=old_m, headers={'Content-Type': old_m.content_type})
    new_resp = requests.post(news_url, data=new_m, headers={'Content-Type': new_m.content_type})

    return old_resp.json(), new_resp.json()


def cmp_dict(src_data,dst_data):   
    try:
        assert type(src_data) == type(dst_data)
    except AssertionError:
        print("type: '{}' != '{}'".format(type(src_data), type(dst_data)))

    if isinstance(src_data,dict):
        for key in src_data:                
            try:
                assert key in dst_data  
            except AssertionError:
                print("key : '{}' 不在 dst_data 中".format(key) )
                continue

            cmp_dict(src_data[key],dst_data[key])    

    elif isinstance(src_data,list):                      
        for src_list, dst_list in zip(sorted(src_data), sorted(dst_data)):
            cmp_dict(src_list, dst_list)

    else:
        try:
            assert src_data == dst_data
        except AssertionError:
            print("value '{}' != '{}'".format(src_data, dst_data))
 

if __name__ == "__main__":

    path = os.path.abspath(os.path.dirname(__file__)) + r'/docs/data.xlsx'
    datalist = Read_xls(path, u"委托下单").read()

    for data in datalist:

        if data['rowNum'] % 10 or data['rowNum'] == 2: 
            # 登录
            old_login_resp = login(old_url)
            new_login_reso = login(news_url)

        # 替换{{}}参数
        old_data = data['body'].replace("{{thread_id}}", str(old_login_resp['data']['thread_id'])).replace("{{session_no}}", str(old_login_resp['data']['session_no']))
        new_data = data['body'].replace("{{thread_id}}", str(new_login_reso['data']['thread_id'])).replace("{{session_no}}", str(new_login_reso['data']['session_no']))

        print("\n***************正在输出第 %s 条用例的对比结果******************" %(data['rowNum']-1))
        old_resp, new_resp = requets(old_data, new_data)
        print("老接口的响应数据为 : \n{}".format(old_resp))
        print("新接口的响应数据为 : \n{}".format(new_resp))

        print("\n老接口和新接口的对比结果为 : ")
        # 对比数据
        cmp_dict(old_resp, new_resp)
        print("\n")
        
        import pdb; pdb.set_trace()
        

