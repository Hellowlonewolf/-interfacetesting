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

del_uesr=del_name()
@pytest.fixture(scope='class')
def test_del_precondition():
    # 私聊
    with requests.post(sendmsg_url(), headers=chat_header(), json={
        "from": del_uesr,
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
        assert_correct_method(send_s)
    # 群聊
    with requests.post(sendmsg_url(), headers=chat_header(), json={
        "from": del_uesr,
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

@allure.feature('删除私聊消息用例')
class TestDelMsg:
    '''
    删除私聊消息用例
    '''

    @allure.story('删除私聊消息')
    def test_del_msg(self, test_del_precondition):
        '''
        :param test_del_precondition:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data={
            "from": del_uesr,
            "to": "p:dc_ceshi"
        }
        with allure.step("请求参数:%s请求地址:%s" % (data,delmsg_url())):
            with requests.post(delmsg_url(), headers=chat_header(), json=data)as delmsg:
                with allure.step("返回参数:%s" % delmsg.json()):
                    assert_correct_method(delmsg)
                    if delmsg.json()['code'] == 1:
                        # 查询私聊是否还存在消息
                        get_data={
                            "from": del_uesr,
                            "to": ["p:dc_ceshi"],
                            "startTime": request_time() - 10,
                            "endTime": request_time() + 10,
                            "limit": 10
                        }
                        with allure.step("查询私聊是否还存在消息请求参数:%s请求地址:%s" % (get_data, getmsg_url())):
                            with requests.post(getmsg_url(), headers=chat_header(), json=get_data) as getmsg:
                                with allure.step("返回参数:%s" % getmsg.json()):
                                    if getmsg.json()['code'] == 1:
                                        for key in getmsg.json():
                                            if key == 'data':
                                                assert False, '删除消息失败,账号还存在消息%s' % getmsg.json()['data']
                    # 查看群聊消息是否还在
                    with requests.post(getmsg_url(), headers=chat_header(), json={
                        "from": del_uesr,
                        "to": ["s:dc_ceshi"],
                        "startTime": request_time() - 10,
                        "endTime": request_time() + 10,
                        "limit": 10
                    }) as getmsg_s:
                        if 'data' not in getmsg_s.json():
                            assert False, '删除群聊消息,私聊消息也被删除'

    @allure.story('参数为空')
    def test_null_data(self, test_del_precondition):
        '''
        :param test_del_precondition:
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={}
        with allure.step("请求参数:%s 请求地址%s" % (data,delmsg_url())):
            with requests.post(delmsg_url(), headers=chat_header(), json=data)as del_null_msg:
                with allure.step("返回参数:%s" % del_null_msg.json()):
                    assert_error_method(del_null_msg)


