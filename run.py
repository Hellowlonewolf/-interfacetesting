#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/08/13
# @Author  : zxp

import pytest, os, time
from chat_method.processing_data import result_data

curPath = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    pytest.main(['-v', '-s', curPath + '/test_cases', '--alluredir', curPath + '/report/report', '--clean-alluredir'])
    code = 1
    new = time.time()
    while code:
        try:
            exists = os.path.exists((curPath + '/report/report'))
            if exists == True:
                os.system(
                    'allure generate ' + curPath + '/report/report -o ' + curPath + '/report/allure-reports/ --clean')
                break
            else:
                pytest.main(['-v', '-s', curPath + '/test_cases', '--alluredir', curPath + '/report/report',
                             '--clean-alluredir'])
        except Exception:
            print('等待生成静态文件...')
        finally:
            time.sleep(1)
            if int(time.time()) - int(new) > 8:
                code = 0
                print('报告生成失败')
    # 生成ci判断结果
    code = 1
    new = time.time()
    while code:
        try:
            result_data()
            break
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            if int(time.time()) - int(new) > 8:
                code = 0
