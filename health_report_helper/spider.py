# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2020 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# spider.py 2021/9/11 13:01
import json
import requests
import config
import logging

from uniform_login.uniform_login_spider import login
import utils


def get_apply_list(cookies):
    try:
        response = requests.get(
            url='http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do',
            headers=config.HEADERS,
            cookies=cookies
        )
        data = json.loads(response.text)
        return data['data']
    except Exception as e:
        logging.exception(e)
        raise e


def do_apply(cookies, WID, location):
    try:
        response = requests.get(
            url='http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/saveApplyInfos.do',
            params=dict(
                WID=WID,
                IS_TWZC=1,
                IS_HAS_JKQK=1,
                JRSKMYS=1,
                JZRJRSKMYS=1,
                CURR_LOCATION=location
            ),
            headers=config.HEADERS,
            cookies=cookies
        )
        if not (response.status_code == 200 and '成功' in response.text):
            raise Exception('健康填报失败')
    except Exception as e:
        logging.exception(e)
        raise e


def main(username, password, location):
    # 登录
    cookies = login(username, password, 'http://ehallapp.nju.edu.cn/xgfw/sys/yqfxmrjkdkappnju/apply/getApplyInfoList.do')
    # 获取填报列表
    apply_list = get_apply_list(cookies)
    if not apply_list[0]['TBRQ'] == utils.get_GMT8_str('%Y-%m-%d'):
        raise Exception("当日健康填报未发布")
    # 填报当天
    do_apply(cookies, apply_list[0]['WID'], location)