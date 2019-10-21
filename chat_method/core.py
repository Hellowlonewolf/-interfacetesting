# -*- coding: UTF-8 -*-
# @Time    : 2019/08/12
# @Author  : zxp

'''
    测试数据,
    非必要不要进行修改
    以免用例出现问题
'''

import time,requests
from random import randint
from chat_base.config import sendmsg_url,chat_header
def username():
    '''
    发送消息用例名称
    :return:
    '''
    return 'test_'+str(randint(100,900))+''


def count_name():
    '''
    查询消息用例名称
    :return:
    '''
    return 'count_'+str(randint(100,900))+''


def del_name():
    '''
    删除消息用例名称
    :return:
    '''
    return 'del_'+str(randint(100,900))+''


def forbid_name():
    '''
    添加禁言名称
    :return:
    '''
    return 'forbid_'+str(randint(100,900))+''


def get_forbid_name():
    '''
    查询禁言用户名称
    :return:
    '''
    return ['getborbid_'+str(randint(100,900))+'', 'getborbid_'+str(randint(100,900))+'']

def del_forbid_name():
    '''
       解除用户禁言
    :return:
    '''
    return 'delforbid_'+str(randint(100,900))+''


def get_forbid_record_name():
    '''
    查看禁言记录
    :return:
    '''
    return 'get_delforbid_'+str(randint(100,900))+''

def del_forbid_recore_name():
    '''
    删除禁言记录
    :return:
    '''
    return 'get_recore_'+str(randint(100,900))+''

def request_time():
    '''
    请求时间戳
    :return:
    '''
    return time.time()


def null_regionid():
    '''
    请求头null_regionid
    :return:
    '''
    header = {
        'Trace-Id': '123213',
    }
    return header


def assert_correct_method(jsondata):
    '''
    正常条件下断言
    :param json:
    :return:
    '''

    assert jsondata.json()['code'] == 1, 'code不为1,当前code为:%s' % jsondata.json()['code']
    assert jsondata.json()['info'] == 'ok', 'info不为ok,当前info为:%s' % jsondata.json()['info']


def assert_getmsg_method(jsondata):
    assert jsondata.json()['code'] == 1, 'code不为1,当前code为:%s' % jsondata.json()['code']
    assert jsondata.json()['info'] == 'ok', 'info不为ok,当前info为:%s' % jsondata.json()['info']
    assert jsondata.json()['data'][0]['Body'] == '正常发送消息', 'text返回值有误,当前text为:%s' % jsondata.json()['data']['text']


def assert_forbid_method(jasondata):
    '''
    禁言时断言状态
    :param json:
    :return:
    '''
    assert jasondata.json()['code'] == 486, 'code不为486,当前code为:%s' % jasondata.json()['code']
    assert jasondata.json()['info'] == 'forbidden speak', 'info返回值有误,当前info为:%s' % jasondata.json()['info']


def assert_sendmsg_method(jsondata):
    '''
    发送消息验证文本断言
    :param json:
    :return:
    '''
    assert jsondata.json()['code'] == 1, 'code不为1,当前code为:%s' % jsondata.json()['code']
    assert jsondata.json()['info'] == 'ok', 'info不为ok,当前info为:%s' % jsondata.json()['info']
    assert jsondata.json()['data']['text'] == '正常发送消息', 'text返回值有误,当前text为:%s' % jsondata.json()['data']['text']


def assert_error_method(jasondata):
    '''
    断言错误返回值
    :param jasondata:
    :return:
    '''
    assert jasondata.json()['code'] == -1, 'code不为1,当前code为:%s' % jasondata.json()['code']
    assert jasondata.json()['info'] == 'the param ill', 'info返回有误,当前info为:%s' % jasondata.json()['info']


def condition():
    '''
    敏感词测试条件验证
    :return:
    '''
    data = {
        "from": 'garbFilter',
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
    with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
        if send_s.json()['data']['text'] == '****':
            return False
        else:
            return True

def condition_data():
    '''
    敏感词测试条件验证数据返回
    :return:
    '''
    data = {
        "from": 'garbFilter',
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
    with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
        return [send_s.json(),data]


def Advertising_conditions():
    '''
    发送广告被封禁
    :return:
    '''
    for i in range(6):
        with requests.post(sendmsg_url(), headers=chat_header(), json={
            "from": 'Advertising_data',
            "to": "p:dc_ceshi",
            "msgType": 1,
            "body": "加我q q1139747920",
            "ext": {
                "key": "value"
            },
            "garbFilter": True,
            "wordFilter": True,
            "time": request_time()
        }) as send_s:
            assert send_s.status_code == 200
    data = {
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
    with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
        if send_s.json()['code'] == 486:
            return False
        else:
            return True

def Advertising_data():
    '''
    发送广告被封禁数据返回
    :return:
    '''
    data = {
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
    with requests.post(sendmsg_url(), headers=chat_header(), json=data) as send_s:
        return [send_s.json(),data]

