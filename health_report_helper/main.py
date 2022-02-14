# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright 2021 zhangt2333. All Rights Reserved.
# Author-Github: github.com/zhangt2333
# main.py 2021/9/11 13:01
import json
import re
import sys
import logging
import time
import random
from datetime import datetime

import config
import spider
import utils

if __name__ == '__main__':
    if len(sys.argv) > 1:
        config.data = json.loads(re.sub('#(.*)\n', '\n', sys.argv[1]).replace("'", '"'))
    if utils.get_GMT8_timestamp() > utils.str_to_timestamp(config.data['deadline'], '%Y-%m-%d'):
        logging.info("超出填报日期")
        exit(-1)
    # retry mechanism
    for _ in range(5):
        try:
            random.seed(datetime.now())
            sleeptime=random.randint(10,19)
            logging.info(str(sleeptime))
            spider.main(config.data['username'], config.data['password'], config.data['location'])
            break
        except Exception as e:
            logging.exception(e)
            time.sleep(5)