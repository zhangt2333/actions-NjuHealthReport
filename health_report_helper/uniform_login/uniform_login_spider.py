# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Copyright 2021 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# uniform_login_spider.py 2021/9/11 13:01
import base64
import random
import re

import requests
from Cryptodome.Cipher import AES


def password_encrypt(text: str, key: str):
    """translate from encrypt.js"""
    _rds = lambda length: ''.join([random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(length)])
    pad = lambda s: s + (len(key) - len(s) % len(key)) * chr(len(key) - len(s) % len(key))
    text = pad(_rds(64) + text).encode("utf-8")
    aes = AES.new(str.encode(key), AES.MODE_CBC, str.encode(_rds(16)))
    return str(base64.b64encode(aes.encrypt(text)), 'utf-8')


# example: login(username='your-student-id', password='your-password', to_url='https://ehall.nju.edu.cn:443/login?service=https://ehall.nju.edu.cn/ywtb-portal/official/index.html')
def login(username, password, to_url):
    """登录并返回JSESSIONID"""
    url = 'https://authserver.nju.edu.cn/authserver/login?service=' + to_url
    lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt, cookies = getLoginCasData(url)
    data = dict(
        username=username,
        password=password_encrypt(password, pwdDefaultEncryptSalt),
        lt=lt,
        dllt=dllt,
        execution=execution,
        _eventId=_eventId,
        rmShown=rmShown,
    )
    try:
        response = requests.post(
            url=url,
            headers=HEADERS_LOGIN,
            data=data,
            cookies=cookies,
        )
        for resp in response.history:
            if resp.cookies.get('MOD_AUTH_CAS'):
                return resp.cookies
        if response.cookies.get('JSESSIONID'):
            return response.cookies
        raise Exception("login error")
    except execution as e:
        raise e


def getLoginCasData(url):
    """返回CAS数据和初始JSESSIONID"""
    try:
        response = requests.get(
            url=url,
            headers=HEADERS_LOGIN
        )
        if response.status_code == 200:
            # 获取 html 中 hidden 的表单 input
            lt = re.findall('name="lt" value="(.*?)"', response.text)[1]
            dllt = re.findall('name="dllt" value="(.*?)"', response.text)[1]
            execution = re.findall('name="execution" value="(.*?)"', response.text)[1]
            _eventId = re.findall('name="_eventId" value="(.*?)"', response.text)[1]
            rmShown = re.findall('name="rmShown" value="(.*?)"', response.text)[1]
            pwdDefaultEncryptSalt = re.findall('id="pwdDefaultEncryptSalt" value="(.*?)"', response.text)[0]
            return lt, dllt, execution, _eventId, rmShown, pwdDefaultEncryptSalt, response.cookies
    except Exception as e:
        raise e


HEADERS_LOGIN = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
}
