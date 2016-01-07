#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright 2015 john <john@apple.local>
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
from lib.list_parse import ListParse

DEBUG = True
DISPLAY = Display(visible=0, size=(720, 1280))
DISPLAY.start()
DRIVER = webdriver.Chrome()
DRIVER.set_page_load_timeout(10)

REDIS_FROM = TaskCache(db = 0)
REDIS_TO = TaskCache(db = 1)

DOWNLOAD_PATH = '/home/john/wechat/download'

LIST_PARSE = ListParse(REDIS_TO)

def log(msg):
    if DEBUG:
        print msg
    pass

def get(url):
    try:
        before = time.time() * 1000
        DRIVER.get(url)
        after = time.time() * 1000
        take_time = after - before
        log("Spider takes time: %d millisecond." % take_time)
        html = (DRIVER.page_source).encode("utf-8")
        return html
    except Exception, e:
        print e
        return None

def get_url_type(url):
    if url.find('/mp/getmasssendmsg') >= 0:
        return 'list'
    elif re.compile(r'^/s\?__biz').match(url) is not None:
        return 'article'
    else:
        return None

def list_process():
    pass

def article_process():
    pass


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
    article_id = params.get('sn') or []
    uin = params.get('uin') or []
    # get type from url
    wechat_type = get_url_type(path)

    if 'list' == wechat_type:
        log("download list page")
        html = get(url)
        if html != None:
            filename = DOWNLOAD_PATH + "/" + date_str + "/list/" + official_account_id[0] + ".html"

            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

            try:
                with open(filename, "w") as f:
                    f.write(html)
                    f.close()
                    msg_list = LIST_PARSE.get_first_group_urls(html)
                    LIST_PARSE.push_msg_list_cache(msg_list)
            except Exception, e:
                print e

    elif 'article' == wechat_type:
        log("download article page")
        html = get(url)
        filename = DOWNLOAD_PATH + "/" + date_str + "/article/" + official_account_id[0] + "/" + article_id[0] + ".html"

        try:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, "w") as f:
                f.write(html)
                f.close()
        except Exception, e:
            print e

    else:
        log("Unkown wechat type")

    time.sleep(1)
    continue

DRIVER.close()














