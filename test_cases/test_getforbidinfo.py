#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/15
# @Author  : zxp
import requests, os, sys, pytest,allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from chat_base.config import *
from chat_method.core import *

forbid_time = int(request_time() + 100)

forbid_name = get_forbid_name()


@pytest.fixture(scope='class')
def test_add_forbid():
    for i in range(2):
        with requests.post(addforbid_url(), headers=chat_header(), json=({
            "roleId": forbid_name[i],
            "text": "广告",
            "desc": "辱骂他人",
            "status": 1,
            "expiryTime": forbid_time
        }))as add_forbid:
            assert_correct_method(add_forbid)
    yield test_add_forbid
    for i in range(2):
        with requests.post(delforbidinfo_url(), headers=chat_header(), json={
            "roleId": forbid_name[i]
        })as delfor:
            assert_correct_method(delfor)

@allure.feature('查询禁言用例')
class TestGetForbidInfo:
    '''
    查询禁言用例
    '''

    @allure.story('查询禁言')
    def test_get_forbid(self, test_add_forbid):
        '''

        :param test_add_forbid:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'ID': '5d5ce0b37dbc2635ec331a5c', 'RoleID': 'getborbid_196', 'Text':
         '广告', 'Status': 1, 'Time': 1566367923, 'ExpiryTime': 1566368024, 'Desc': '辱骂他人'}]}
        '''
        data= {   "roleId": forbid_name[0],
            "page": 1,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data,getforbid_url())):
            with requests.post(getforbid_url(), headers=chat_header(), json=data)as get_forbid:
                with allure.step("返回参数:%s" % get_forbid.json()):
                    assert_correct_method(get_forbid)
                    assert get_forbid.json()['data'][0]['RoleID'] == forbid_name[0]
                    assert get_forbid.json()['data'][0]['Text'] == '广告'
                    assert get_forbid.json()['data'][0]['ExpiryTime'] == forbid_time

    @allure.story('验证limit功能')
    def test_verify_limit(self, test_add_forbid):
        '''
        :param test_add_forbid:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'ID': '5d5ce1717dbc2635ec33211c', 'RoleID': 'getborbid_793',
        'Text': '广告', 'Status': 1, 'Time': 1566368113, 'ExpiryTime': 1566368214, 'Desc': '辱骂他人'},
         {'ID': '5d5ce1717dbc2635ec332124', 'RoleID': 'getborbid_525', 'Text': '广告', 'Status': 1, 'Time': 1566368113, 'ExpiryTime': 1566368214, 'Desc': '辱骂他人'}]}

        '''
        data=  {
            "limit": 2
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbid_url())):
            with requests.post(getforbid_url(), headers=chat_header(), json=data)as get_forbid:
                with allure.step("返回参数:%s" % get_forbid.json()):
                    assert_correct_method(get_forbid)
                    assert len(get_forbid.json()['data']) == 2, 'limi获取消息条数有误,当前条数应为:%s' % len(get_forbid.json()['data'])

    @allure.story('获取当前封禁全部用户')
    def test_null_body(self, test_add_forbid):
        '''
        :param test_add_forbid:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data={}
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbid_url())):
            with requests.post(getforbid_url(), headers=chat_header(), json=data)as get_forbid:
                with allure.step("返回参数:%s" % get_forbid.json()):
                    assert_correct_method(get_forbid)
                    for i in get_forbid.json()['data']:
                        if 'ExpiryTime' in i:
                            if int(request_time()) > i['ExpiryTime']:
                                assert False, '存在封禁时间已经到期还能被查询出来的用户'
