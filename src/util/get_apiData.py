#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


class generate_param():

    def _generate_random_str(self, randomlength=16):
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

    def _generate_valueArea(self, valueAreavalue):
        '''
        参数有默认值时, 遍历每个值和添加一个无效等价类
        '''
        valueArealist = []
        # 遍历取值的区间, 把每个元素都添加进list
        for v in valueAreavalue:
            valueArealist.append(v)
        # 超出等价范围的值
        valueArealist.append("hello")

        return valueArealist

    def str_Generate(self, param):
        '''
        string生成参数方法
        '''
        paramlist = []
        # 把默认正确值放在list的第一个
        paramlist.append(param['default'])
        # 空字符
        paramlist.append("")
        # 类型非string
        paramlist.append(100)

        if param['valueArea']:
            # 有取值区间
            # _valueArealist = _generate_valueArea(param['valueArea'])
            for v in param['valueArea']:
                if param['default'] != v:
                    paramlist.append(v)
            paramlist.append(param['valueArea'][-1] + 'abc')
        else:
            # 生成指定长度的随机字符串
            if param['lenght']:
                _generatelist = self._generate_random_str(param['lenght'])
            else:
                _generatelist = self._generate_random_str()

            paramlist.extend(_generatelist)

        # print(paramlist)
        return paramlist

    def Int_Generate(self, param):
        intparamlist = []
        # 默认正确值
        intparamlist.append(param['default'])
        intparamlist.append(param['default'] + 0.11)
        intparamlist.append(0)
        intparamlist.append(-1)

        if param['valueArea']:
            # 遍历所有等价类
            for v in param['valueArea']:
                if v != param['default']:
                    intparamlist.append(v)

            # 添加一个无效等价类, list中最后一个值加10
            intparamlist.append(param['valueArea'][-1] + 10)


        # print(intparamlist)
        return intparamlist

    def get_api_key_data(self, api_document):
        API_KEY_DATA = {}

        for param in api_document['body']:
            if param['generate'] == "false":
                # 转移成list类型, 便于生成测试数据
                API_KEY_DATA[param['key'].strip()] = [param['default']]
                continue
            elif param['type'] == "string":
                API_KEY_DATA[param['key'].strip()] = self.str_Generate(param)
            elif param['type'] == "int":
                API_KEY_DATA[param['key'].strip()] = self.Int_Generate(param)
            else:
                print("没有定义 {} 类型".format(param['type']))


        return API_KEY_DATA



