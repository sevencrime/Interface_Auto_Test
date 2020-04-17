#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class generate_param():

    def __generate_random_str(self, randomlength=16):
        """
        生成指定长度的随机字符串
        """
        _generatelist = []
        random_str = ''
        random_str_many = ''
        random_str_little = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789_-=+()@#$%^&*?'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]

        random_str_many = random_str + base_str[random.randint(0, length)]
        random_str_little = random_str[:random.randint(1, randomlength-1)]
        _generatelist.append(random_str)
        _generatelist.append(random_str_many)
        _generatelist.append(random_str_little)

        return _generatelist

    def __str_Generate(self, param):
        '''
        生成string数据
        '''
        paramlist = []
        # 把默认正确值放在list的第一个
        paramlist.append(param.get("default"))
        # 空字符
        paramlist.append("")
        # 类型非string
        paramlist.append(100)

        if param.get("valueArea"):
            # 有取值区间
            # _valueArealist = _generate_valueArea(param.get("valueArea"))
            for v in param.get("valueArea"):
                if param.get("default") != v:
                    paramlist.append(v)
            paramlist.append(param.get("valueArea")[-1] + 'abc')
        else:
            # 生成指定长度的随机字符串
            if param.get("lenght"):
                _generatelist = self.__generate_random_str(param.get("lenght"))
            else:
                _generatelist = self.__generate_random_str()

            paramlist.extend(_generatelist)

        # print(paramlist)
        return paramlist

    def __Int_Generate(self, param):
        '''
        生成int类型数据
        '''
        intparamlist = []
        # 默认正确值
        intparamlist.append(param.get("default"))
        intparamlist.append(str(param.get("default")))
        intparamlist.append(param.get("default") + 0.11)
        intparamlist.append(0)
        intparamlist.append(-1)

        if param.get("valueArea"):
            # 遍历所有等价类
            for v in param.get("valueArea"):
                if v != param.get("default"):
                    intparamlist.append(v)

            # 添加一个无效等价类, list中最后一个值加10
            intparamlist.append(param.get("valueArea")[-1] + 10)

        # print(intparamlist)
        return intparamlist

    def __float_Generate(self, param):
        '''
        生成float类型的数据
        '''
        floatparamlist = []
        floatparamlist.append(param.get("default"))
        floatparamlist.append(str(param.get("default")))
        floatparamlist.append(0)
        floatparamlist.append(-1)
        floatparamlist.append(random.uniform(0, 100))

        return floatparamlist

    def get_api_key_data(self, api_document):
        API_KEY_DATA = {}   # 存放每个参数生成的测试数据列表
        requiredParam = {}  # 存放所有必填参数, key == default
        non_requiredParam = {} # 存放所有非必填参数

        for param in api_document.get('body'):
            if param.get("generate"):
                # 转移成list类型, 便于生成测试数据
                API_KEY_DATA[param.get("key").strip()] = [param.get("default")]
                continue

            if param.get("type") == "string":
                API_KEY_DATA[param.get("key").strip()] = self.__str_Generate(param)
            elif param.get("type") == "int":
                API_KEY_DATA[param.get("key").strip()] = self.__Int_Generate(param)
            elif param.get("type") == "float":
                API_KEY_DATA[param.get("key").strip()] = self.__float_Generate(param)
            else:
                print("没有定义 {} 类型".format(param.get("type")))

            if param.get("isempty") == "Y":
                requiredParam[param.get("key")] = param.get("default")
            elif param.get("isempty") == "N":
                non_requiredParam[param.get("key")] = param.get("default")
            else:
                print("不支持了")


        # print(requiredParam)
        # print(non_requiredParam)

        delparamlist = []   

        for key in requiredParam.keys():
            # 遍历必填参数列表, 依次删除一个key
            delparam = requiredParam.copy()
            del delparam[key]
            delparamlist.append(delparam)

        # print(delparamlist)

        return API_KEY_DATA, delparamlist



if __name__ == "__main__":
    import json
    with open("../api_json/{}.json".format("API_301"), encoding='utf-8') as f:
        apis = json.load(f)

    g = generate_param()
    API_KEY_DATA, delparamlist = g.get_api_key_data(apis)
    print(API_KEY_DATA)


    list1 = []
    for k, v in API_KEY_DATA.items():
        dict1 = {}
        __newDATA = API_KEY_DATA.copy()
        del __newDATA[k]

        for newkey, newvalue in __newDATA.items():
            dict1[newkey] = newvalue[0]

        for sonV in v:
            itdict = dict1.copy()
            itdict[k] = sonV

            list1.append(itdict)

    # print(list1)
    # print(list1.__len__())