#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/12
# @Author  : zxp

import requests, os, sys, pytest,allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from chat_base.config import *
from chat_method.core import *




user=username()
@allure.feature('发送消息用例')
class TestSendMsg:
    '''
    发送消息用例
    '''

    @allure.story('发送群发消息')
    def test_verify_send_s(self):
        '''
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 's:dc_ceshi_5d5ceb4e9f58c70001c47270', 'text': '正常发送消息'}}
        '''
        data= {
            "from": user,
            "to": "s:dc_ceshi",
            "msgType": 1,
            "body": "正常发送消息",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data,sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_sendmsg_method(send_s)

    @allure.story('发送私聊消息')
    def test_verify_send_private(self):
        '''
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 'p:test_510dc_ceshi_5d5ceb8f9f58c70001c47284', 'text': '正常发送消息'}}
        '''
        data= {
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "正常发送消息",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_sendmsg_method(send_s)
    @allure.story('请求头regionid为空')
    def test_null_region(self):
        '''
        :return:
        {'code': -1, 'info': 'No Set logical_region_id'}
        '''
        data=null_regionid()
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=data, json={
                "from": user,
                "to": "p:dc_ceshi",
                "msgType": 1,
                "body": "请求头regionid为空",
                "ext": {
                    "key": "value"
                },
                "garbFilter": True,
                "wordFilter": True,
                "time": request_time()
            }) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert send_s.json()['code'] == -1, 'code不为-1,当前code为:%s' % send_s.json()['code']
                    assert send_s.json()['info'] == 'No Set logical_region_id', 'info不为No Set logical_region_id,当前info为:%s' % \
                                                                                send_s.json()['info']

    @allure.story('body 与 ext 同时为空')
    def test_null_body_ext(self):
        '''
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data= {
            "from": user,
            "to": "p:dc_ceshi"
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=null_regionid(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_error_method(send_s)

    @allure.story('body 为空')
    def test_nullbody(self):
        '''
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 's:dc_ceshi_5d5cec509f58c70001c472bf', 'text': ''}}
        '''
        data=  {
            "from": user,
            "to": "s:dc_ceshi",
            "msgType": 1,
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_correct_method(send_s)
                    assert send_s.json()['data']['text'] == '', 'text返回值有误,当前text为:%s' % send_s.json()['data']['text']

    @allure.story('敏感词过滤关闭')
    def test_wordFilter_false(self):
        '''
        {
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "test",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": False,
            "time": request_time()
        }
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 'p:test_272dc_ceshi_5d5cec949f58c70001c472d3', 'text': 'test'}}
        '''
        data={
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "test",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": False,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_correct_method(send_s)
                    assert send_s.json()['data']['text'] == 'test', 'text返回值有误,当前text为:%s' % send_s.json()['data']['text']
    @pytest.mark.skipif(condition(),
                        reason="请求参数:"+str(condition_data()[1])+"\r\n敏感词测试条件不满足跳过此用例,条件请求返回值:"+str(condition_data()[0])+"")
    @allure.story('敏感词过滤开启')
    def test_wordfilter_true(self):
        '''
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 'p:test_290dc_ceshi_5d5cece89f58c70001c472e7', 'text': '****'}}
        '''
        data={
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "test",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_correct_method(send_s)
                    assert send_s.json()['data']['text'] == '****', 'text返回值有误,当前text为:%s' % send_s.json()['data']['text']

    @allure.story('广告词检测关闭')
    @pytest.mark.repeat(6)
    def test_garbfilter_false(self):
        '''
        {
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "加我q q1139747920",
            "ext": {
                "key": "value"
            },
            "garbFilter": False,
            "wordFilter": True,
            "time": request_time()
        }
        :return:
        {'code': 1, 'info': 'ok', 'data': {'msg_id': 'p:test_590dc_ceshi_5d5ced159f58c70001c47300', 'text': '加我q q1139747920'}}
        '''
        data={
            "from": user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "加我q q1139747920",
            "ext": {
                "key": "value"
            },
            "garbFilter": False,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_correct_method(send_s)
                    assert send_s.json()['data']['text'] == '加我q q1139747920', 'text返回值有误,当前text为:%s' % send_s.json()['data'][
                        'text']

    @pytest.fixture
    def test_garbfilter_preposition(self):
        '''
        广告词检测前置条件
        :return:
        '''
        yield self.test_garbfilter_preposition

        # 清除测试数据-解除禁言
        with requests.post(delforbidinfo_url(), headers=chat_header(), json={
            "roleId": 'Advertising_data'
        })as delfor:
            assert_correct_method(delfor)

    @pytest.mark.skipif(Advertising_conditions(),
                        reason="请求参数:" + str(Advertising_data()[1]) + "\r\n发送广告禁言测试条件不满足跳过此用例,条件请求返回值:" + str(
                            Advertising_data()[0]) + "")
    @allure.story('禁言后发言')
    def test_garbfilter_true(self, test_garbfilter_preposition):
        '''
        :return:
        {'code': 486, 'info': 'forbidden speak'}
        '''
        data={
            "from": 'Advertising_data',
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
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_forbid_method(send_s)

    @allure.story('发送错误参数类型')
    def test_error_parameter(self,):
        '''
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={
            "from": user,
            "to": "ps:dc_ceshi",
            "msgType": 1,
            "body": "正常发送消息",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, sendmsg_url())):
            with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
                with allure.step("返回参数:%s" % send_s.json()):
                    assert_error_method(send_s)
