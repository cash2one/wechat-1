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
import pdb
from selenium import webdriver

from lib.task_cache import TaskCache

REDIS_FROM = TaskCache(db = 0)
REDIS_TO = TaskCache(db = 1)
PHANTOMJS = 'http://192.168.7.111:9999'
DOWNLOAD_PATH = '/home/john/wechat/download'
DRIVER = webdriver.PhantomJS("/home/john/opt/phantomjs/bin/phantomjs")

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

def phantomjs(url):
    DRIVER.get(url)
    html = DRIVER.page_source
    return html

# data = dict(url="http://www.linuxeden.com")

# html = post(PHANTOMJS, data)
# print html

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
        data = dict(url = url)
        html = post(PHANTOMJS, data)
        filename = DOWNLOAD_PATH + "/" + date_str + "/list/" + official_account_id[0] + ".html"

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "w") as f:
            f.write(html)
            f.close()
    elif 'article' == wechat_type:
        data = dict(url = url)
        html = post(PHANTOMJS, data)
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














