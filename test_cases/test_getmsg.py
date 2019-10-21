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
count_user=count_name()

@pytest.fixture(scope='class')
def test_get_precondition():
    for i in range(2):
        with requests.post(sendmsg_url(), headers=chat_header(), json={
            "from": count_user,
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "正常发送消息",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }) as send_s:
            assert_sendmsg_method(send_s)
    with requests.post(sendmsg_url(), headers=chat_header(), json={
        "from": count_user,
        "to": "s:dc_ceshi",
        "msgType": 1,
        "body": "群聊消息",
        "ext": {
            "key": "value"
        },
        "garbFilter": True,
        "wordFilter": True,
        "time": request_time()
    }) as send_s:
        assert_correct_method(send_s)
        assert send_s.json()['data']['text'] == '群聊消息', 'text返回值有误,当前text为:%s' % send_s.json()['data']['text']

@allure.feature('获取消息用例')
class TestGetMsg:
    '''
    获取消息用例
    '''
    @allure.story('获取消息')
    def test_correct_get(self, test_get_precondition):
        '''
        :param precondition:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'MsgID': 'p:dc_ceshicount_746_5d5ce7799f58c70001c4724a',
        'From': 'count_746', 'To': 'dc_ceshi', 'MsgType': 1, 'Body': '正常发送消息', 'Ext': {'key': 'value'}, 'Time': 1566369657.482258},
        {'MsgID': 'p:dc_ceshicount_746_5d5ce7799f58c70001c47249', 'From': 'count_746', 'To': 'dc_ceshi', 'MsgType': 1,
        'Body': '正常发送消息', 'Ext': {'key': 'value'}, 'Time': 1566369657.4443762}]}

        '''
        data= {
            "from": count_user,
            "to": ["p:dc_ceshi"],
            "startTime": request_time() - 10,
            "endTime": request_time() + 10,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as getmsg:
                with allure.step("返回参数:%s" % getmsg.json()):
                    assert_getmsg_method(getmsg)
                    assert len(getmsg.json()['data']) >= 2, 'limi获取消息条数有误,当前条数应为:%s' % len(getmsg.json()['data'])

    @allure.story('过滤非必填参数')
    def test_no_required(self,  test_get_precondition):
        '''

        :param precondition:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'MsgID': 'p:dc_ceshicount_576_5d5ce7d19f58c70001c4724d', 'From': 'count_576',
        'To': 'dc_ceshi', 'MsgType': 1, 'Body': '正常发送消息', 'Ext': {'key': 'value'}, 'Time': 1566369746.0853312},
        {'MsgID': 'p:dc_ceshicount_576_5d5ce7d19f58c70001c4724c', 'From': 'count_576', 'To': 'dc_ceshi', 'MsgType': 1,
        'Body': '正常发送消息', 'Ext': {'key': 'value'}, 'Time': 1566369746.0473883}]}
        '''
        data= {
            "from": count_user,
            "to": ["p:dc_ceshi"],
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as no_required:
                with allure.step("返回参数:%s" % no_required.json()):
                    assert_getmsg_method(no_required)

    @allure.story('过滤必填参数')
    def test_required(self,test_get_precondition):
        '''
        :param precondition:
        :return:
        {'code': -1, 'info': 'runtime error: index out of range'}
        '''
        data={
            "startTime": request_time() - 10,
            "endTime": request_time() + 10,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as required:
                with allure.step("返回参数:%s" % required.json()):
                    assert required.json()['code'] == -1, 'code不为-1,当前code为:%s' % required.json()['code']
                    assert required.json()['info'] == 'runtime error: index out of range', 'info返回有误,当前info为:%s' % \
                                                                                           required.json()['info']

    @allure.story('验证时间范围功能')
    def test_verify_time(self,test_get_precondition):
        '''
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data= {
            "from": count_user,
            "to": ["p:dc_ceshi"],
            "startTime": request_time() + 10000,
            "endTime": request_time() + 10001,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as gettime:
                with allure.step("返回参数:%s" % gettime.json()):
                    assert_correct_method(gettime)

    @allure.story('获取群聊消息')
    def test_get_group_chat(self,test_get_precondition):
        '''
        :param precondition:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'MsgID': 's:dc_ceshi_5d5ce92e9f58c70001c47254', 'From': 'count_263',
        'To': 'dc_ceshi', 'MsgType': 1, 'Body': '群聊消息', 'Ext': {'key': 'value'}, 'Time': 1566370095.1075342}]}
        '''
        data=    {
            "to": ["s:dc_ceshi"],
            "startTime": request_time() - 10,
            "endTime": request_time() + 10,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as getmsg:
                with allure.step("返回参数:%s" % getmsg.json()):
                    assert_correct_method(getmsg)
                    assert getmsg.json()['data'][0]['Body'] == '群聊消息', 'text返回值有误,当前text为:%s' % getmsg.json()['data']['text']

    @allure.story('错误参数类型')
    def test_error_parameter(self,test_get_precondition):
        '''
        :param test_get_precondition:
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={
            "from": count_user,
            "to": ["sss:dc_ceshi"],
            "startTime": request_time() - 10,
            "endTime": request_time() + 10,
            "limit": 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getmsg_url())):
            with requests.post(getmsg_url(), headers=chat_header(), json=data) as getmsg:
                with allure.step("返回参数:%s" % getmsg.json()):
                    assert_error_method(getmsg)
