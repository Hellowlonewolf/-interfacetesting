#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/14
# @Author  : zxp

import requests, os, sys, pytest, allure

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from chat_base.config import *
from chat_method.core import *

get_record_time = int(request_time())

get_forbid_record_user = get_forbid_record_name()


@pytest.fixture(scope='class')
def test_getforbidrecord():
    # 生出测试数据添加测试账号禁言
    with requests.post(addforbid_url(), headers=chat_header(), json=({
        "roleId": get_forbid_record_user,
        "text": "广告",
        "desc": "辱骂他人",
        "status": 1,
        "expiryTime": get_record_time
    }))as add_forbid:
        assert_correct_method(add_forbid)
    yield test_getforbidrecord
    # 清除数据 解除禁言
    with requests.post(delforbidinfo_url(), headers=chat_header(), json={
        "roleId": get_forbid_record_user
    })as delfor:
        assert_correct_method(delfor)


@allure.feature('查看禁言记录用例')
class TestGetForbidRecord:
    '''
    查看禁言记录
    '''

    @allure.story('查看禁言记录')
    def test_get_record(self, test_getforbidrecord):
        '''
        :param test_getforbidrecord:
        :return:
        {'code': 1, 'info': 'ok', 'data': [{'ID': '5d5ceff47dbc2635ec33a319', 'RoleID': 'get_delforbid_254', 'Type': 1,
        'Desc': '辱骂他人', 'Time': 1566371828, 'ExpiryTime': 1566371828}, {'ID': '5d5ceff47dbc2635ec33a31b', '
        RoleID': 'get_delforbid_254', 'Type': 2, 'Desc': '禁言时间到期', 'Time': 1566371828}]}
        '''
        data = {
            "roleId": get_forbid_record_user,
            "page": 1,
            'limit': 10,
            'startTime': get_record_time - 10,
            'endTime': get_record_time + 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbidrecord_url())):
            with requests.post(getforbidrecord_url(), headers=chat_header(), json=data)as get_record:
                with allure.step("返回参数:%s" % get_record.json()):
                    assert_correct_method(get_record)
                    assert get_record.json()['data'][0]['RoleID'] == get_forbid_record_user

    @allure.story('空body')
    def test_null_body(self):
        '''
        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data = {
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbidrecord_url())):
            with requests.post(getforbidrecord_url(), headers=chat_header(), json=
            data)as get_error_record:
                with allure.step("返回参数:%s" % get_error_record.json()):
                    assert_error_method(get_error_record)

    @allure.story('验证条数')
    def test_verify_limit(self):
        '''

        :return:
        {'code': 1, 'info': 'ok', 'data':
        [{'ID': '5d5ce6477dbc2635ec334b63', 'RoleID': 'get_delforbid_698', 'Type': 2, 'Desc': '禁言时间到期', 'Time': 1566369351}]}

        '''
        data=      {
            "roleId": get_forbid_record_user,
            "page": 1,
            'limit': 1,
            'startTime': get_record_time - 10,
            'endTime': get_record_time + 10
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbidrecord_url())):
            with requests.post(getforbidrecord_url(), headers=chat_header(), json=
            data)as get_limit:
                with allure.step("返回参数:%s" % get_limit.json()):
                    assert_correct_method(get_limit)
                    if len(get_limit.json()['data']) > 1:
                        assert False, 'linmit设置为1,查询结果不为一条禁言记录'

    @allure.story('验证查询时间功能')
    def test_verify_time(self):
        '''
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data= {
            "roleId": get_forbid_record_user,
            "page": 1,
            'limit': 10,
            'startTime': get_record_time + 100,
            'endTime': get_record_time + 101
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, getforbidrecord_url())):
            with requests.post(getforbidrecord_url(), headers=chat_header(), json=
           data)as get_record:
                with allure.step("返回参数:%s" % get_record.json()):
                    assert_correct_method(get_record)
                    if 'data' in get_record.json():
                        assert False, '时间范围功能没有生效,改时间测试账号范围应无封禁记录'
