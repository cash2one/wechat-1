#coding:utf-8
import pcap
import dpkt
import sys
import re

pc = pcap.pcap("wlan0")
pc.setfilter('tcp and src 192.168.7.103')
# f = open('test.pcap')
# pc = dpkt.pcap.Reader(f)

def handle_get(headerString):
    result = {}
    headerLines = headerString.split('\r\n')

    for line in headerLines:
        if 0 != len(line):
            key, value = line.split(' ', 1)
            key = key.strip().replace(':', '')
            value = value.strip().replace(' HTTP/1.1', '')
            result[key] = value
    return result

def handle_post(headerString):
    result = {}
    headerLines = headerString.split('\r\n')

    for line in headerLines:
        if 0 != len(line):
            key, value  = line.split(' ', 1)

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

                        if result.get('Referer') is not None:
                            print result['Referer']
                        else:
                            # get article list
                            if result.get('GET').find('/mp/getmasssendmsg?') >= 0:
                            print 'http://' + result.get('Host') + result.get('GET')

                            # article page
                            article_re = re.compile(r'^/s\?__biz')
                            article_match = article_re.match(result.get('GET'))
                            if article_match is not None:
                                print 'http://' + result.get('Host') + result.get('GET')

if __name__ == '__main__':
    main()
