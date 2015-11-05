import urllib
import urllib2
import json

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

url = 'http://192.168.7.111:9999'

data = dict(url="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzA5NDA4MjU1MQ==&uin=MTIzOTkyMDUzOQ%3D%3D&key=b410d3164f5f798eaea088915ebdf095ab4c3ad0d70d782e55ee558e9935a7e0e641ec59b712391416d6e521f7dc48e3&devicetype=android-19&version=26030531&lang=zh_CN&nettype=WIFI&pass_ticket=hiX%2F8kekKqVM%2Bf%2BrdJxCC4YGXM1V40gcMvHgD4%2FcahCs3ypFueuboAfu4VEWhXPq")

html = post(url, data)
f = open('./baidu.html', 'w')
f.write(html)
f.close()