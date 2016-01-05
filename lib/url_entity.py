#coding:utf-8
"""
URL entity object
"""
import urlparse

class UrlEntity(object):
    """docstring for UrlEntity"""
    def __init__(self, url):
        super(UrlEntity, self).__init__()
        self.url = url
        self.url_parse_object = urlparse.urlparse(url)
        self.scheme = self.url_parse_object.scheme
        self.netloc = self.url_parse_object.netloc
        self.path = self.url_parse_object.path
        self.params = urlparse.parse_qs(self.url_parse_object.query)

    def get_param(self, key):
        resule = self.params.get(key)
        if (resule == None):
            return resule[0]
        else:
            return None

url = "http://mp.weixin.qq.com/s?__biz=MzAwOTY2ODczOA==&mid=402263400&idx=3&sn=e325163736ce15753f6b92940296a699&scene=4#wechat_redirect"
