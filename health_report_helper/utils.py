# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2021 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# utils.py 2021/9/11 13:01
import datetime
import time


def get_GMT8_timestamp():
    return (datetime.datetime.utcfromtimestamp((time.time())) + datetime.timedelta(hours=8)).timestamp()


def get_GMT8_str(format: str):
    return (datetime.datetime.utcfromtimestamp((time.time())) + datetime.timedelta(hours=8)).strftime(format)


def str_to_timestamp(time_str: str, format: str):
    return int(time.mktime(time.strptime(time_str, format)))