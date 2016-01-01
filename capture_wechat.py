#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright 漏 2015 john <john@apple.local>
#
# Distributed under terms of the MIT license.

"""

"""
import os
import urllib
import urllib2
import json
import time
import urlparse
import datetime
import re

from selenium import webdriver
from pyvirtualdisplay import Display
from lib.task_cache import TaskCache

DISPLAY = Display(visible=0, size=(720, 1280))
DISPLAY.start()
DRIVER = webdriver.Chrome()

REDIS_FROM = TaskCache(db = 0)
REDIS_TO = TaskCache(db = 1)

DOWNLOAD_PATH = '/home/john/wechat/download'

while True:
    url = REDIS_FROM.get_random()
    if url == None:
        print "Not url task."
        time.sleep(1)
        continue

    url_parse_object = urlparse.urlparse(url)
    path = url_parse_object.path
    params = urlparse.parse_qs(url_parse_object.query)
    wechat_type = ''
    date_str = datetime.datetime.now().strftime('%Y%m%d')

    official_account_id = params.get('__biz') or []
    uin = params.get('uin') or []

    if path.find('/mp/getmasssendmsg') >= 0:
        wechat_type = 'list'
    elif re.compile(r'^/s\?__biz').match(path) is not None:
        wechat_type = 'article'
    else:
        wechat_type = None

    if 'list' == wechat_type:
        print "download list page"
        DRIVER.get(url)
        html = (DRIVER.page_source).encode("utf-8")
        filename = DOWNLOAD_PATH + "/" + date_str + "/list/" + official_account_id[0] + ".html"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w") as f:
            f.write(html)
            f.close()

    elif 'article' == wechat_type:
        DRIVER.get(url)
        html = (DRIVER.page_source).encode("utf-8")
        filename = DOWNLOAD_PATH + "/" + date_str + "/article/" + official_account_id[0] + ".html"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w") as f:
            f.write(html)
            f.close()
    else:
        print "Unkown wechat type"

    time.sleep(0.5)
    print "==="
    pass

DRIVER.close()














