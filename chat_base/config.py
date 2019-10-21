# -*- coding: UTF-8 -*-
# @Time    : 2019/08/12
# @Author  : zxp


def chat_url():
    '''
    内网测试地址
    :return:
    '''
    url = 'http'
    return url


def chat_header():
    '''
    请求头
    :return:
    '''
    header = {
        'Content-Type': 'application/json',
        'Trace-Id': '123213',
        'Logical-Region-Id': '1202'
    }
    return header


def sendmsg_url():

    return chat_url() + '/path'


def getmsg_url():

    return chat_url() + '/path'


def delmsg_url():

    return chat_url() + '/path'


def addforbid_url():

    return chat_url() + '/path'


def getforbid_url():

    return chat_url()+'/path'

def delforbidinfo_url():

    return chat_url() + '/path'

def getforbidrecord_url():

    return chat_url() + '/path'

def removerecord_url():

    return chat_url()+'/path'