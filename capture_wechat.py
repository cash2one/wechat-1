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

import config
from selenium import webdriver
from pyvirtualdisplay import Display
from lib.task_cache import TaskCache
from lib.list_parse import ListParse
from lib.models import OfficialAccount

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

def save_html(html, filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    try:
        with open(filename, "w") as f:
            f.write(html)
            f.close()
            return True
    except Exception, e:
        print e
        return False

def article_process(url):
    url_parse_object = urlparse.urlparse(url)
    path = url_parse_object.path
    params = urlparse.parse_qs(url_parse_object.query)
    date_str = datetime.datetime.now().strftime('%Y%m%d')

    official_account_id = params.get('__biz') or []
    group_id = params.get('mid') or []
    index = params.get('idx') or []
    article_id = params.get('sn') or []
    uin = params.get('uin') or []
    file_name = official_account_id[0] + '_' + group_id[0] + '_' + index[0] + '_' + article_id[0]

    html = get(url)
    filename = DOWNLOAD_PATH + "/" + date_str + "/article/" + official_account_id[0] + "/" + file_name + ".html"

    save_html(html, filename)
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
        # get list html
        html = get(url)

        if html != None:
            filename = DOWNLOAD_PATH + "/" + date_str + "/list/" + official_account_id[0] + ".html"
            wechat_code = official_account_id[0]
            official_account = OfficialAccount.where(wechat_code = wechat_code).getone()

            if official_account is not None:
                first_group_date = LIST_PARSE.get_first_group_datetime(html)

                reg = re.match(ur"([\d]+)年([\d]+)月([\d]+)日([\d]+):([\d]+)", first_group_date)

                last_datetime = datetime.datetime(int(reg.group(1)), \
                    int(reg.group(2)), int(reg.group(3)), int(reg.group(4)), \
                    int(reg.group(5)), 0)

                if last_datetime > official_account.last_article_time:
                    log("First article time is great then last_article_time, download first group articles")
                    official_account.last_article_time = last_datetime
                    official_account.save()

                    save_html(html, filename)
                    msg_list = LIST_PARSE.get_first_group_urls(html)
                    #LIST_PARSE.push_msg_list_cache(msg_list)
                    for msg_url in msg_list:
                        log("process article page")
                        article_process(msg_url)
                        pass
                else:
                    log("Do not process article")
                    pass
            else:
                log("wechat_code is not found in mysql, " + wechat_code)

    # article process
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














