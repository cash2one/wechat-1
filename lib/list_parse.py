# -*- coding: utf-8 -*-
from pyquery import PyQuery
import task_cache

class ListParse(object):
    """docstring for ListParse"""
    def __init__(self, redis = task_cache.TaskCache(), is_push_to_redis = True):
        super(ListParse, self).__init__()
        self.redis = redis
        self.is_push_to_redis = is_push_to_redis

    def push_to_redis(self, url):
        if self.is_push_to_redis:
            self.redis.push(url)
            pass

    def get_first_group_urls(self, html):
        html = PyQuery(html)
        msg_page = html('.msg_page')[0].getchildren()

        # first group
        msg_list = msg_page[0]
        children = msg_list.getchildren()
        # msg header
        msg_list_hd = children[0]
        first_group_msg_date = msg_list_hd.getchildren()[0].text
        # msg body
        msg_list_bd = children[1]

        # first group message list
        first_group_msg_list = msg_list_bd.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()

        # get url array from first group message list
        urls = self.iterate_msg_list(first_group_msg_list)

        return urls

    def iterate_msg_list(self, msg_list_html):
        urls = []
        hrefs = ""

        for item in msg_list_html:
            if "{http://www.w3.org/1999/xhtml}a" == item.tag:
                hrefs = item.get("hrefs")
                if hrefs is not None:
                    urls.append(hrefs)
            elif "{http://www.w3.org/1999/xhtml}div" == item.tag:
                hrefs = item.getchildren()[0].get("hrefs")
                if hrefs is not None:
                    urls.append(hrefs)
            else:
                continue

        return urls

    def push_msg_list_cache(self, msg_list):
        for item in msg_list:
            self.push_to_redis(item)

f = open("/Users/john/MzA3ODU4NjgwMw==.html")
list_parse = ListParse()
print list_parse.get_first_group_urls(f.read())

