#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_toolbelt import MultipartEncoder
from commond.read_xls import Read_xls
import os
from jira import JIRA

old_url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/Handle.aspx'
news_url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/NewGateWay.aspx'

def login(url):
    querystr = '{"account":"3001331112","password":"abcd1234","branch_no":"","account_type":"8","MF":201,"op_station":"ZctPcY8BCaT6tCmxYYPc6TwcnPKCTxpQ","op_entrust_way":"A","language_type":"1"}'
    m = MultipartEncoder(fields={'QueryString': querystr})
    i = 0 
    while i < 3:
        try:
            resp = requests.post(url, data=m, headers={'Content-Type' : m.content_type})
            assert resp.json()['error_info'].strip() == "ok"
            # print("\n登录接口返回的数据为 : {}".format(resp.json()))
            return resp.json()
        except AssertionError:
            i += 1
            print("登录接口网络错误, 重试第 {} 次".format(i))
            if i == 2:
                print("算了, 手动请求看是不是挂了吧")
                import pdb; pdb.set_trace()


def find_history():
    url = 'http://trade-route-develop.ntdev.be:8080/GXSocket/Handle.aspx'
    loginresp = login(url)

    data = {
        "MF": 509,
        "fund_account" : "3001331112",
        "stock_code" : "",
        "from_trade_date" : "2020-03-10",
        "to_trade_date" : "2020-03-18",
        "op_station" : "",
    }

    data['session_no'] = loginresp['data']['session_no']
    data['thread_id'] = loginresp['data']['thread_id']

    order_no_dict = {
        "0" : [] , 
        "1" : [] , 
        "2" : [] , 
        "3" : [] , 
        "4" : [] , 
        "5" : [] , 
        "6" : [] , 
        "7" : [] , 
        "8" : [] , 
        "9" : [] , 
        "A" : [] , 
        "B" : [] , 
        "C" : [] , 
        "D" : [] , 
        "W" : [] , 
        "X" : [] , 
        "E" : [] , 
        "F" : [] , 
        "G" : [] , 
        "H" : [] , 
        "J" : [] , 
        "Q" : [] , 
    }


    m = MultipartEncoder(fields={'QueryString' : "{}".format(data)})

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Openwave', 'Content-Language': 'en-US'}
    try:
        resp=requests.post(url,data=m, headers={'Content-Type': m.content_type})
        response = resp.json()
        assert response['error_info'] == 'ok'
    except Exception as e:
        raise e

    for d in response['data']['history_order_list']:
        order_no_dict[d['entrust_status']].append(d['order_no'])


    # order_no_dict = {'0': [], '1': ['12403', '12401', '12400', '12398', '12397', '12396', '12395', '12394', '12393', '12392', '12387', '12386', '12385', '12384', '12383', '12382', '12381', '12380', '12379', '12378', '12377', '12376', '12375', '12374', '12373', '12372', '12371', '12370', '12369', '12368', '12367', '12366', '12365', '12364', '12363', '12362', '12361', '12360', '12359', '12358', '12357', '12356', '12355', '12354', '12353', '12352', '12351', '12350', '12349', '12348', '12347', '12346', '12345', '12344', '12343', '12342', '12341', '12340', '12339', '12338', '12337', '12336', '12335', '12334', '12333', '12332', '12331', '12330', '12329', '12328', '12327', '12326', '12325', '12324', '12321', '12320', '12317', '12314', '12313', '12312', '12311', '12310', '12309', '12308', '12307', '12304', '12303', '12302', '12299', '12298', '12297', '12296', '12293', '12292', '12291', '12290', '12289', '12287', '12286', '12281', '12280', '12279', '12278', '12277', '12276', '12275', '12274', '12260', '12259', '12258', '12257', '12256', '12255', '12254', '12253', '12241', '12240', '12239', '12238', '12202', '12201', '12198', '12196', '12195', '12194', '12193', '12192', '12191', '12190', '12189', '12187', '12186', '12179', '12178', '12176', '12175', '12174', '12173', '12172', '12171', '12170', '12169', '12168', '12167', '12166', '12165', '12164', '12163', '12162', '12161', '12160', '12159', '12158', '12157', '12156', '12155', '12154', '12153', '12152', '12151', '12150', '12149', '12148', '12147', '12146', '12145', '12144', '12143', '12142', '12141', '12140', '12139', '12138', '12137', '12136', '12135', '12134', '12133', '12132', '12131', '12130', '12129', '12128', '12127', '12126', '12125', '12124', '12123', '12122', '12121', '12120', '12119', '12118', '12117', '12116', '12115', '12114', '12113', '12112', '12111', '12110', '12109', '12108', '12107', '12106', '12105', '12104', '12103', '12102', '12099', '12098', '12097', '12096', '12095', '12094', '12093', '12092', '12089', '12088', '12087', '12086', '12085', '12084', '12083', '12082', '12081', '12080', '12079', '12078', '12077', '12076', '12075', '12074', '12073', '12072', '12071', '12070', '12069', '12068', '12067', '12066', '12065', '12064', '12063', '12062', '12061', '12060', '12059', '12058', '12057', '12056', '12055', '12054', '12053', '12052', '12051', '12050', '12049', '12048', '12047', '12046', '12045', '12044', '12041', '12040', '12039', '12038', '12037', '12036', '12035', '12034', '12031', '12030', '12029', '12028', '12027', '12026', '12025', '12024', '12023', '12022', '12021', '12020', '12019', '12018', '12017', '12016', '12015', '12014', '12013', '12012', '12011', '12010', '12009', '12008', '12007', '12006', '12005', '12004', '12003', '12002', '12001', '12000', '11999', '11998', '11997', '11996', '11995', '11994', '11993', '11992', '11991', '11990', '11989', '11988', '11987', '11986', '11985', '11984', '11983', '11982', '11981', '11980', '11979', '11978', '11977', '11976', '11975', '11974', '11973', '11972', '11971', '11970', '11969', '11968', '11967', '11966', '11965', '11964', '11963', '11962', '11961', '11960', '11959', '11958', '11957', '11956', '11955', '11954', '11953', '11952', '11951', '11950', '11949', '11948', '11945', '11944', '11942', '11941', '11940', '11939', '11938', '11937', '11934', '11933', '11932', '11931', '11930', '11929', '11926', '11925', '11924', '11923', '11922', '11921', '11920', '11919', '11918', '11917', '11916', '11915', '11914', '11913', '11912', '11911', '11910', '11909', '11908', '11907', '11906', '11905', '11904', '11903', '11902', '11901', '11898', '11897', '11896', '11895', '11894', '11893', '11892', '11891', '11888', '11885', '11884', '11883', '11882', '11881', '11880', '11879', '11878', '11875', '11874', '11873', '11872', '11871', '11870', '11869', '11868', '11867', '11866', '11865', '11864', '11863', '11862', '11861', '11860', '11859', '11858', '11857', '11856', '11851', '11850', '11849', '11848', '11847', '11844', '11843', '11835', '11834', '11833', '11826', '11801', '11800', '11799', '11798', '11796', '11770', '11769', '11765', '11763', '11762', '11734', '11617', '11615', '11578', '11490', '11441', '11437', '11436', '11430', '11429', '11428', '11427', '11426', '11425', '11424', '11423', '11422', '11421', '11420', '11419', '11418', '11417', '11416', '11415', '11414', '11413', '11412', '11411', '11410', '11408', '11341', '11340', '11339', '11338', '11337', '11336', '11334', '11333', '11332', '11331', '11325', '11324', '11322', '11321', '11320', '11319', '11318', '11317', '11310', '11309', '11308', '11307', '11304', '11303', '11302', '11301', '11300', '11299', '11298', '11296', '11295', '11294', '11293', '11292', '11291', '11290', '11289', '11288', '11287', '11286', '11285', '11284', '11281', '11280', '11279', '11278', '11277', '11276', '11275', '11274', '11273', '11272', '11268', '11267', '11266', '11265', '11264', '11263', '11262', '11261', '11260', '11259', '11258', '11257', '11256', '11255', '11254', '11253', '11252', '11251', '11250', '11249', '11248', '11247', '11246', '11245', '11243', '11242', '11241', '11239', '11211', '11196', '11194', '11190'], '2': [], '3': [], '4': [], '5': [], '6': ['11618', '11616', '11591', '11590', '11589', '11588', '11587', '11475', '11473', '11472', '11471', '11470', '11440', '11439', '11438', '11435', '11434', '11433', '11432', '11409', '11323', '11313', '11312', '11311', '11306', '11297', '11203', '11092'], '7': ['12414', '12413', '11645', '11644', '11643', '11642'], '8': ['12415', '11646', '11638', '11637', '11581', '11579', '11577', '11516', '11474', '11443', '11442', '11431', '11316', '11228', '11195', '11114', '11112', '11110', '11109', '11108', '11107', '11106', '11105', '11104', '11103', '11102', '11101', '11100', '11099', '11098', '11097', '11096', '11095', '11090', '11089', '11088', '11062'], '9': [], 'A': [], 'B': [], 'C': [], 'D': [], 'W': [], 'X': [], 'E': [], 'F': ['12402', '12399', '12316', '12315', '12306', '12305', '12101', '12100', '12091', '12090', '12043', '12042', '12033', '12032', '11947', '11946', '11936', '11935', '11928', '11927', '11900', '11899', '11890', '11889', '11887', '11886', '11877', '11876', '11619', '11614', '11592', '11584', '11407', '11406', '11405', '11404', '11403', '11402', '11401', '11400', '11399', '11398', '11396', '11395', '11394', '11393', '11392', '11391', '11390', '11389', '11388', '11387', '11386', '11385', '11384', '11383', '11382', '11381', '11380', '11379', '11378', '11377', '11376', '11375', '11374', '11373', '11372', '11371', '11370', '11369', '11368', '11367', '11366', '11365', '11364', '11363', '11362', '11361', '11360', '11359', '11358', '11357', '11356', '11355', '11354', '11353', '11352', '11351', '11350', '11349', '11348', '11347', '11346', '11345', '11344', '11343', '11342', '11330', '11329', '11328', '11327', '11326', '11189', '11188', '11179'], 'G': [], 'H': [], 'J': [], 'Q': ['11613', '11305']}

    return order_no_dict


def requets(old_data, new_data):

    # m = MultipartEncoder(fields={'QueryString' : "{'MF': 301, 'fund_account': '3001331112', 'exchange_type': 'K', 'stock_account': '3001331112', 'stock_code': '00008', 'entrust_amount': 10000, 'entrust_price': 0.047, 'entrust_bs': 'B', 'entrust_prop': 'e', 'op_station': 'isX5db4FstXj2MdW3weZGcpAktjHG4nM', 'session_no': 0}"})
    old_m = MultipartEncoder(fields={'QueryString' : old_data})
    new_m = MultipartEncoder(fields={'QueryString' : new_data})
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Openwave', 'Content-Language': 'en-US'}
    i = 0
    while i < 3:
        try:
            old_resp = requests.post(old_url, data=old_m, headers={'Content-Type': old_m.content_type})
            print(old_resp.elapsed.total_seconds())
            break
        except Exception as e:
             i += 1
             print("request超时重试")

    k = 0
    while k < 3:
        try:
            new_resp = requests.post(news_url, data=new_m, headers={'Content-Type': new_m.content_type})
            print(new_resp.elapsed.total_seconds())
            break
        except Exception as e:
            k += 1
            print("request超时重试")


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
        try:
            assert src_data.__len__() == dst_data.__len__()
        except AssertionError:
            print("src_data的个数为 : {}, dst_data的个数为 : {}".format(src_data.__len__(), dst_data.__len__()))
            return True

        try:
            # list嵌套dict排序sorted(lis, key=lambda k: k['x'])
            for src_list, dst_list in zip(sorted(src_data, key=lambda k: k['create_time']), sorted(dst_data, key=lambda k: k['create_time'])):
                cmp_dict(src_list, dst_list)
        except TypeError:
            for src_list, dst_list in zip(src_data, dst_data):
                cmp_dict(src_list, dst_list)

    else:
        try:
            assert src_data == dst_data
        except AssertionError:
            print("value '{}' != '{}'".format(src_data, dst_data))
 

def create_jira_eddid(log_info, sheetname, title, body, old_resp, new_resp):
    options = {'server': 'http://172.16.10.243:8080/'}
    jira = JIRA(options, basic_auth=log_info)

    summary = "[新老接口对比][{sheetname}]{title}, 对比不一致".format(sheetname=sheetname, title=title)
    description = '''
    [请求参数]
    {body}

    [老接口响应数据]
    {old_resp}

    [新接口响应数据]
    {new_resp}

    [期望结果]
    新老接口, 响应数据一致
    '''.format(body=body, old_resp=old_resp, new_resp=new_resp)


    issue_dict = {
        'project': {'key': 'AYER'},  # 项目
        'issuetype': {'id': '10004'},  # 问题类型
        'priority': {'id': '3'},  # 优先级
        'summary': summary,  # 问题主题
        'assignee': {'name': 'wuchaozhen'},  # 经办人
        'description': description,  # 问题描述
        'customfield_10203' : {'id' : '10112'}, # 严重级别
    }
    rsp = jira.create_issue(issue_dict)
    issue = jira.issue(rsp)
    print(issue.key, issue.fields.summary, issue.fields.status)
    jira.close()

def reduce_dict(longdict):
    # 截取json中的一段
    reduces = {}
    for k, v in longdict.items():
        # print(k, v)
        if k == 'data':
            reduces[k] = {}
            reduces[k]['history_order_list'] = longdict['data']['history_order_list'][0:2]
        else:
            reduces[k] = v


    return reduces


if __name__ == "__main__":
    sheetname = "委托下单"
    path = os.path.abspath(os.path.dirname(__file__)) + r'/docs/data.xlsx'
    datalist = Read_xls(path, sheetname).read()

    if sheetname == "委托撤单" : 
        old_orderDict = find_history()

    for data in datalist:

        if data['rowNum'] < 101 :
            continue

        # 登录, 每次请求都登录, 防止登录过期
        old_login_resp = login(old_url)
        new_login_resp = login(news_url)

        
        old_entrust_no = ""
        new_entrust_no = ""

        if sheetname == "委托撤单":

            if data['name'].find("拒绝") != -1:
                old_entrust_no = old_orderDict['F'][0]
                new_entrust_no = old_orderDict['F'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['F'].remove(old_orderDict['F'][0])
                    old_orderDict['F'].remove(old_orderDict['F'][1])

            elif data['name'].find("已撤") != -1:
                old_entrust_no = old_orderDict['6'][0]
                new_entrust_no = old_orderDict['6'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['6'].remove(old_orderDict['6'][0])
                    old_orderDict['6'].remove(old_orderDict['6'][1])

            elif data['name'].find("部成") != -1:
                old_entrust_no = old_orderDict['7'][0]
                new_entrust_no = old_orderDict['7'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['7'].remove(old_orderDict['7'][0])                
                    old_orderDict['7'].remove(old_orderDict['7'][1])                

            elif data['name'].find("已成") != -1:
                old_entrust_no = old_orderDict['8'][0]
                new_entrust_no = old_orderDict['8'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['8'].remove(old_orderDict['8'][0])                
                    old_orderDict['8'].remove(old_orderDict['8'][1])        

            elif data['name'].find("待报") != -1:
                old_entrust_no = old_orderDict['1'][0]
                new_entrust_no = old_orderDict['1'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['1'].remove(old_orderDict['1'][0])                
                    old_orderDict['1'].remove(old_orderDict['1'][1])                

            else:
                old_entrust_no = old_orderDict['Q'][0]
                new_entrust_no = old_orderDict['Q'][1]
                if '"cancel_type": "0"' in data['body']:
                    # 撤单, 用完的批号删除
                    old_orderDict['Q'].remove(old_orderDict['Q'][0])                
                    old_orderDict['Q'].remove(old_orderDict['Q'][1])   



        # 替换{{}}参数
        old_data = data['body'].replace("{{thread_id}}", str(old_login_resp['data']['thread_id'])).replace("{{session_no}}", str(old_login_resp['data']['session_no'])).replace("{{entrust_no}}", '"{}"'.format(str(old_entrust_no))).replace(" ", "").replace("\n", "")
        new_data = data['body'].replace("{{thread_id}}", str(new_login_resp['data']['thread_id'])).replace("{{session_no}}", str(new_login_resp['data']['session_no'])).replace("{{entrust_no}}", '"{}"'.format(str(new_entrust_no))).replace(" ", "").replace("\n", "")

        # import pdb; pdb.set_trace()
        

        print("\n***************正在输出第 {} 条用例的对比结果, Excel第 {} 行******************".format(data['rowNum']-1, data['rowNum']))
        old_resp, new_resp = requets(old_data, new_data)

        print("\n用例标题 : {}\n".format(data['name']))
        print("老接口的响应数据为 : \n{}".format(old_resp))
        print("新接口的响应数据为 : \n{}".format(new_resp))

        print("\n老接口和新接口的对比结果为 : ")
        # 对比数据
        cmp_dict(old_resp, new_resp)
        print("\n")
        
        if data['rowNum'] > 1 :
            import pdb; pdb.set_trace()
        

# create_jira_eddid(("zhengqinyuan", "12345678"), sheetname, data['name'], old_data, old_resp, new_resp)
# create_jira_eddid(("zhengqinyuan", "12345678"), sheetname, data['name'], old_data, old_resp, reduce_dict(new_resp))