#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright 漏 2015 john <john@apple.local>
#
# Distributed under terms of the MIT license.

"""
Get url from redis 0, capture wechat page, and save it to file
"""
import os
import urllib
import urllib2
import json
import time
import urlparse
import datetime
import time
import re

from selenium import webdriver
from pyvirtualdisplay import Display
from lib.task_cache import TaskCache

DEBUG = True
DISPLAY = Display(visible=0, size=(720, 1280))
DISPLAY.start()
DRIVER = webdriver.Chrome()
DRIVER.set_timeout(3)
DRIVER.set_page_load_timeout(3)

REDIS_FROM = TaskCache(db = 0)
REDIS_TO = TaskCache(db = 1)

DOWNLOAD_PATH = '/home/john/wechat/download'

def log(msg):
    if DEBUG:
        print msg
    pass

def get(url):
    before = time.time()
    DRIVER.get(url)
    after = time.time()
    take_time = after - before
    log("Spider takes time: %d secode." % take_time)
    html = (DRIVER.page_source).encode("utf-8")
    return html

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
        html = get(url)
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














