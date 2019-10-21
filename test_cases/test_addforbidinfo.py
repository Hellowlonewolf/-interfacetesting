#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/14
# @Author  : zxp
import requests, os, sys, pytest,allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from chat_base.config import *
from chat_method.core import *

forbid_user=forbid_name()
@pytest.fixture(scope='class')
def test_del():
    '''
    重复禁言调用
    :return:

    '''
    with requests.post(addforbid_url(), headers=chat_header(), json=({
        "roleId": forbid_user,
        "text": "f**k",
        "desc": "辱骂他人",
        "status": 1,
        "expiryTime": request_time() + 100
    }))as add_forbid:
        assert_correct_method(add_forbid)
    yield test_del

    with requests.post(delforbidinfo_url(), headers=chat_header(), json={
        "roleId": forbid_user
    })as delfor:
        assert_correct_method(delfor)

@allure.feature('添加禁言用例')
class TestAddForbidInfo:
    '''
    添加禁言
    '''

    @pytest.fixture
    def test_delforbidinfo(self):
        '''
        清除测试数据-解除禁言
        {  "roleId": forbid_user }
        :return:
        '''
        yield self.test_delforbidinfo

        with requests.post(delforbidinfo_url(), headers=chat_header(), json={
            "roleId": forbid_user
        })as delfor:
            with allure.step("返回参数:%s" % delfor.json()):
                assert_correct_method(delfor)


    @allure.story('添加禁言')
    def test_add_forbid(self, test_delforbidinfo):
        '''
        :param test_delforbidinfo:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data = {
            "roleId": forbid_user,
            "text": "f**k",
            "desc": "辱骂他人",
            "status": 1,
            "expiryTime": request_time() + 100
        }
        with allure.step("请求参数:%s 请求地址%s"%(data,addforbid_url())):
            with requests.post(addforbid_url(), headers=chat_header(), json=data)as add_forbid:
                with allure.step("返回参数:%s" % add_forbid.json()):
                    assert_correct_method(add_forbid)
                    if add_forbid.json()['code'] == 1:
                        # 发现消息查看是否禁言
                        send_data={
                            "from": forbid_user,
                            "to": "p:dc_ceshi",
                            "msgType": 1,
                            "body": "发送消息",
                            "ext": {
                                "key": "value"
                            },
                            "garbFilter": True,
                            "wordFilter": True,
                            "time": request_time()
                        }
                        with allure.step("发现消息验证禁言请求参数:%s" % send_data):
                            with requests.post(sendmsg_url(), headers=chat_header(), json=send_data) as send_s:
                                with allure.step("返回参数:%s" % send_s.json()):
                                    assert_forbid_method(send_s)

    @allure.story('永久封禁')
    def test_perpetual_forbid(self, test_delforbidinfo):
        '''
        :param test_delforbidinfo:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data= {
            "roleId": forbid_user,
            "text": "f**k",
            "desc": "辱骂他人",
            "status": 1
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, addforbid_url())):
            with requests.post(addforbid_url(), headers=chat_header(), json=data)as add_perpetual_forbid:
                with allure.step("返回参数:%s" % add_perpetual_forbid.json()):
                    assert_correct_method(add_perpetual_forbid)
                    if add_perpetual_forbid.json()['code'] == 1:
                        # 发现消息查看是否禁言
                        with requests.post(sendmsg_url(), headers=chat_header(), json={
                            "from": forbid_user,
                            "to": "p:dc_ceshi",
                            "msgType": 1,
                            "body": "发送消息",
                            "ext": {
                                "key": "value"
                            },
                            "garbFilter": True,
                            "wordFilter": True,
                            "time": request_time()
                        }) as send_s:
                            assert_forbid_method(send_s)

    @allure.story('重复禁言')
    def test_repetition_forbid(self,test_del):
        '''
        :return:
        {'code': 486, 'info': 'forbidden speak'}
        '''
        data={
            "roleId": forbid_user,
            "text": "f**k",
            "desc": "辱骂他人",
            "status": 1,
            "expiryTime": request_time() + 100
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, addforbid_url())):
            with requests.post(addforbid_url(), headers=chat_header(), json=data)as add_forbid:
                with allure.step("返回参数:%s" % add_forbid.json()):
                    assert_forbid_method(add_forbid)

    @allure.story('过滤必传参数')
    def test_not_necessary(self):
        '''

        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data= {
            "text": "f**k",
            "desc": "辱骂他人",
            "expiryTime": request_time() + 100
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, addforbid_url())):
            with requests.post(addforbid_url(), headers=chat_header(), json=data)as not_necessary:
                with allure.step("返回参数:%s" % not_necessary.json()):
                    assert_error_method(not_necessary)




