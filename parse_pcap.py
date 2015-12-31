#coding:utf-8
import pcap
import dpkt
import sys
import re

from lib.task_cache import TaskCache

pc = pcap.pcap("wlan0")
pc.setfilter('tcp and src 192.168.7.102')
# f = open('test.pcap')
# pc = dpkt.pcap.Reader(f)
REDIS_CACHE = TaskCache(db = 0)
USE_CACHE = True
DEBUG = True

def handle_get(headerString):
    result = {}
    headerLines = headerString.split('\r\n')

    for line in headerLines:
        if 0 != len(line):
            try:
                key, value = line.split(' ', 1)
                key = key.strip().replace(':', '')
                value = value.strip().replace(' HTTP/1.1', '')
                result[key] = value
                pass
            except Exception, e:
                print line
                raise
    return result

def handle_post(header_string):
    result = {}
    headerLines = header_string.split('\r\n')

    for line in headerLines:
        if 0 != len(line):
            key, value  = line.split(' ', 1)

def cache(url_string):
    if USE_CACHE:
        REDIS_CACHE.push(list_url)
    pass

def log(info):
    if DEBUG:
        print list_url
    pass

def main():
    for ptime,pdata in pc:
        package = dpkt.ethernet.Ethernet(pdata)

        if package.data.__class__.__name__=='IP':
            ip = '%d.%d.%d.%d' % tuple(map(ord,list(package.data.dst)))
            protocal = package.data.data.__class__.__name__

            if protocal == 'TCP':
                headerBody = package.data.data.data
                headerString = headerBody
                pattern = re.compile(r'.*?\s')
                method = pattern.match(headerString)

                if method is not None:
                    method = method.group(0).strip()
                    if 'GET' == method:
                        result = handle_get(headerString)
                        uri = result.get('GET')

                        # get article list
                        if uri.find('/mp/getmasssendmsg?') >= 0:
                            list_url = 'http://' + result.get('Host') + result.get('GET')
                            log(list_url)
                            cache(list_url)
                            continue

                        # article page
                        elif re.compile(r'^/s\?__biz').match(uri) is not None:
                            article_url = 'http://' + result.get('Host') + result.get('GET')
                            log(article_url)
                            cache(article_url)
                            continue

                        # get pic referer
                        elif result.get('Referer') is not None:
                            referer_url = result['Referer']
                            log(referer_url)
                            cache(referer_url)
                            continue
                        else:
                            continue


if __name__ == '__main__':
    main()
