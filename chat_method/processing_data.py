#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/19
# @Author  : zxp

import json, time, os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]

file_json = rootPath + r'/report/allure-reports/data/categories.json'
summary_file = rootPath + r'/report/allure-reports/widgets/summary.json'
create_time = time.strftime("%Y-%m-%d_%H:%M:%S")


def result_data():
    '''
    判断成功or失败
    :return:
    '''
    exists = os.path.exists((rootPath + '//report//allure-reports'))
    if exists == True:
        json_file = open(file_json, encoding='utf-8')
        setting = json.load(json_file)
        data = setting['children']
        summary_data = open(summary_file, encoding='utf-8')
        setting = json.load(summary_data)
        run_time = str(setting['time']['start'])
        if data == []:
            with open(rootPath + '//result.txt', 'w') as result:
                    result.write('Pass''\r\n''File creation time: ')
                    result.write(create_time)
                    result.write('\r\n')
                    result.write(run_time)
    else:
        raise ValueError('allure静态文件不存在')

