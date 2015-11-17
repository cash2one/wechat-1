#coding=utf-8
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

html = getHtml("http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==&uin=NTE1MzA0MDAw&key=b410d3164f5f798e1bcbec8712c7e6d8f87b26aa31df9b070a883847844191d1b52c1dfb6d03f85c4bce2788d66492d3&devicetype=android-22&version=26030531&lang=en&nettype=WIFI&pass_ticket=A7xb%2F5%2Bp8YEz04%2BVke1ni2MaGpxk0JTamAOjhgY82h9FVDVyar%2B5V6Np7VjFZDvP")

print html

# 文章页面 URL
# http://mp.weixin.qq.com/s?
# __biz=MzIwNzA1MTg0OQ== //公共账号 ID
# &mid=400241523 //应该是一次推送的所有 post 都一样
# &idx=1 //每次都一样
# &sn=839a0693809f801d07fddb979409c427 //article id
# &scene=4 //每次都一样
# &uin=NTE1MzA0MDAw //每次都一样
# &key=04dce534b3b035ef8cad60ddd8e8a9233218b8863370af2424bc2c5f473a95bd6fc862f020b7c986c2e20225ddb9c19e // 前 16 个字符每次一样
# &devicetype=android-22 //每次都一样
# &version=26030531 //每次都一样
# &lang=en //每次都一样
# &nettype=WIFI //每次都一样
# &pass_ticket=A7xb%2F5%2Bp8YEz04%2BVke1ni2MaGpxk0JTamAOjhgY82h9FVDVyar%2B5V6Np7VjFZDvP //每次都一样