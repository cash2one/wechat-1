# -*- coding: utf-8 -*-
from pyquery import PyQuery

class ListParse(object):
    """docstring for ListParse"""
    def __init__(self, html, redis, official_account_id):
        super(ListParse, self).__init__()
        self.html = PyQuery(html)
        self.msg_page = self.html('.msg_page')[0].getchildren()
        self.redis = redis
        self.official_account_id = official_account_id

    def get_first_group_urls(self):
        msg_list = self.msg_page[0]
        children = msg_list.getchildren()
        msg_list_hd = children[0]
        first_group_msg_date = msg_list_hd.getchildren()[0].text
        msg_list_bd = children[1]
        first_group_msg_list = msg_list_bd.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()
        urls = []
        for item in first_group_msg_list:
            if "{http://www.w3.org/1999/xhtml}a" == item.tag:
                urls.append(item.get("hrefs"))
            elif "{http://www.w3.org/1999/xhtml}div" == item.tag:
                urls.append(item.getchildren()[0].get("hrefs"))

        return urls

f = open("/Users/john/workspaces/wechat/tmp/MzAwOTY2ODczOA==.html")
# html = PyQuery(f.read())

# msg_page = html('.msg_page')[0].getchildren()

# for msg_list in msg_page:
#     children = msg_list.getchildren()
#     msg_list_hd = children[0]
#     date = msg_list_hd.getchildren()[0].text
#     msg_list_bd = children[1]
#     first_group_msg_list = msg_list_bd.getchildren()[0].getchildren()[1].getchildren()[0].getchildren()
#     for item in first_group_msg_list:
#         if "{http://www.w3.org/1999/xhtml}a" == item.tag:
#             print item.get("hrefs")
#         elif "{http://www.w3.org/1999/xhtml}div" == item.tag:
#             print item.getchildren()[0].get("hrefs")

list_parse = ListParse(f.read())
print list_parse.get_first_group_urls()

