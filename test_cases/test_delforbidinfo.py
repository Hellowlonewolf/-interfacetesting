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

del_forbid_user = del_forbid_name()


@pytest.fixture(scope='class')
def test_del_forbid():
    '''
    生出测试数据添加测试账号禁言
    :return:
    '''
    with requests.post(addforbid_url(), headers=chat_header(), json=({
        "roleId": del_forbid_user,
        "text": "广告",
        "desc": "辱骂他人",
        "status": 1,
        "expiryTime": request_time() + 100
    }))as add_forbid:
        assert_correct_method(add_forbid)

@allure.feature('解除禁言用例')
class TestDelForbidInfo:
    '''
    解除禁言用例

    '''

    @allure.story('解禁账号')
    def test_del_forbid(self, test_del_forbid):
        '''
        :param test_del_forbid:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data= {
            "roleId": del_forbid_user
        }
        with allure.step("请求参数:%s 请求地址:%s" % (data, delforbidinfo_url())):
            with requests.post(delforbidinfo_url(), headers=chat_header(), json={
                "roleId": del_forbid_user
            })as delfor:
                with allure.step("返回参数:%s" % delfor.json()):
                    assert_correct_method(delfor)
                    # 解除后是否可以正常发言
                    send_data={
                        "from": del_forbid_user,
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
                    with allure.step("发现消息验证是否解禁请求参数:%s请求地址:%s" % (send_data,sendmsg_url())):
                        with requests.post(sendmsg_url(), headers=chat_header(), json=send_data) as send_s:
                            with allure.step("返回参数:%s" % send_s.json()):
                                assert_sendmsg_method(send_s)

    @allure.story('忽略必填参数')
    def test_null_body(self):
        '''
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={        }
        with allure.step("请求参数:%s 请求地址:%s" % (data,delforbidinfo_url())):
            with requests.post(delforbidinfo_url(), headers=chat_header(), json=data)as delfor:
                with allure.step("返回参数:%s" % delfor.json()):
                    assert_error_method(delfor)

    @allure.story('上传错误参数')
    def test_error_body(self):
        '''
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={
            "roleI2d": del_forbid_user
        }
        with allure.step("请求参数:%s 请求地址:%s" % (data, delforbidinfo_url())):
            with requests.post(delforbidinfo_url(), headers=chat_header(), json=data)as delfor2:
                with allure.step("返回参数:%s" % delfor2.json()):
                    assert_error_method(delfor2)
