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
import signal
import sys

import config
from selenium import webdriver
from lib.task_cache import TaskCache
from lib.list_parse import ListParse
from lib.models import OfficialAccount
from lib.log import Log

DEBUG = True
#DISPLAY = Display(visible=0, size=(720, 1280))
#DISPLAY.start()
# Xvfb :99 -ac -screen 0 720x1280x24
DRIVER = webdriver.Firefox()
DRIVER.set_page_load_timeout(45)

REDIS_FROM = TaskCache(db = 0)
REDIS_TO = TaskCache(db = 1)

LIST_PARSE = ListParse(REDIS_TO)

LOGGER = Log("capture")

def log(msg):
    if DEBUG:
        # print msg
        LOGGER.error(msg)
    pass

def get(url):
    try:
        before = time.time() * 1000
        DRIVER.get(url)
        after = time.time() * 1000
        take_time = after - before

        html = (DRIVER.page_source).encode("utf-8")
        html_size = len(html)
        log("Browser takes time: %d millisecond. size: %s" % (take_time, str(html_size)))
        return html
    except Exception, e:
        LOGGER.error(e)
        global DRIVER
        DRIVER.close()
        #global DISPLAY
        #DISPLAY.stop()
        LOGGER.error("Restart browser")
        #DISPLAY.start()
        DRIVER = webdriver.Firefox()
        DRIVER.set_page_load_timeout(45)
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
        LOGGER.error(e)
        return False

def article_process(url):
    try:
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
        filename = config.DOWNLOAD_PATH + "/" + date_str + "/article/" + official_account_id[0] + "/" + file_name + ".html"

        save_html(html, filename)
        pass
    except Exception, e:
        LOGGER.error(e)
        pass

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    DRIVER.close()
    #DISPLAY.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    while True:
        url = REDIS_FROM.get_random()
        if url == None:
            log("Not url task.")
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
                filename = config.DOWNLOAD_PATH + "/" + date_str + "/list/" + official_account_id[0] + ".html"
                wechat_code = official_account_id[0]
                official_account = OfficialAccount.get(OfficialAccount.wechat_code == wechat_code)

                if official_account is not None:
                    first_group_date = LIST_PARSE.get_first_group_datetime(html)

                    if first_group_date is None:
                        log("First group datetime is None.")
                        continue
                    else:
                        reg = re.match(ur"([\d]+)年([\d]+)月([\d]+)日([\d]+):([\d]+)", first_group_date)

                        last_datetime = datetime.datetime(int(reg.group(1)), \
                            int(reg.group(2)), int(reg.group(3)), int(reg.group(4)), \
                            int(reg.group(5)), 0)

                        if last_datetime > official_account.last_article_time:
                            log("First article time is great then last_article_time, download first group articles, wechat code:" + wechat_code)
                            official_account.last_article_time = last_datetime
                            official_account.save()

                            save_html(html, filename)

                            # get article list from html
                            msg_list = LIST_PARSE.get_first_group_urls(html)

                            if msg_list is not None:
                                for msg_url in msg_list:
                                    log("process article page")
                                    article_process(msg_url)
                                    pass
                        else:
                            log("First article time is equal to last_article_time, continue.")
                            pass
                else:
                    log("wechat_code is not found in mysql, " + wechat_code)

        # article process
        elif 'article' == wechat_type:
            log("download article page")
            html = get(url)
            filename = config.DOWNLOAD_PATH + "/" + date_str + "/article/" + official_account_id[0] + "/" + article_id[0] + ".html"

            save_html(html, filename)

        else:
            log("Unkown wechat type")

        time.sleep(1)
        continue

main()

DRIVER.close()
#DISPLAY.stop()














