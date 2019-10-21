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

remove_time=int(request_time())
del_forbid_recore_user=del_forbid_recore_name()
@pytest.fixture(scope='class')
def test_add_forbid_remove():
    # 生出测试数据添加测试账号禁言
    with requests.post(addforbid_url(), headers=chat_header(), json=({
        "roleId": del_forbid_recore_user,
        "text": "广告",
        "desc": "辱骂他人",
        "status": 1,
        "expiryTime":remove_time+10
    }))as add_forbid:
        pass
    #查询禁言记录
    with requests.post(getforbidrecord_url(), headers=chat_header(), json=
    {
        "roleId":  del_forbid_recore_user,
        "page": 1,
        'limit': 10,
    })as get_forbid:
        assert_correct_method(get_forbid)
    yield get_forbid.json()['data'][0]['ID']


@allure.feature('删除禁言记录用例')
class TestRemoveRecord:
    '''
    删除禁言记录用例
    '''

    @allure.story('删除禁言记录')
    def test_removerecord(self,test_add_forbid_remove):
        '''
        :param test_add_forbid_remove:
        :return:
        {'code': 1, 'info': 'ok'}
        '''
        data= {
            'Id':test_add_forbid_remove
        }
        with allure.step("请求参数:%s 请求地址%s" % (data, removerecord_url())):
            with requests.post(removerecord_url(),headers=chat_header(),json=data)as remove:
                with allure.step("返回参数:%s" % remove.json()):
                    assert_correct_method(remove)
                    #解除禁言
                    del_data={
                            "roleId": del_forbid_recore_user
                        }
                    with allure.step("解除禁言请求参数:%s 请求地址%s" % (del_data, removerecord_url())):
                        with requests.post(delforbidinfo_url(), headers=chat_header(), json=del_data)as delfor:
                            with allure.step("返回参数:%s" % delfor.json()):
                                assert_correct_method(delfor)
                        get_data={
                            "roleId": del_forbid_recore_user,
                            "page": 1,
                            "limit": 10
                        }
                        with allure.step("解除禁言请求参数:%s 请求地址%s" % (get_data,getforbid_url())):
                            with requests.post(getforbid_url(), headers=chat_header(), json=get_data)as get_forbid:
                                with allure.step("返回参数:%s" % get_forbid.json()):
                                    assert_correct_method(get_forbid)
                                    # print('data数据-----',get_forbid.json()['data'])
                                    # for i  in range(len(get_forbid.json()['data'])):
                                    #     if test_add_forbid_remove  in  get_forbid.json()['data'][i]['ID']:
                                    #         assert False,'删除失败禁言记录还存在'

    @allure.story('参数为空')
    def test_null_body(self):
        '''

        :return:
        {'code': -1, 'info': 'the param ill'}
        '''
        data={}
        with allure.step("请求参数:%s 请求地址%s" % (data, removerecord_url())):
            with requests.post(removerecord_url(), headers=chat_header(), json=data)as remove_null:
                with allure.step("返回参数:%s" % remove_null.json()):
                    assert_error_method(remove_null)


