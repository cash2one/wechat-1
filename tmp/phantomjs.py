from tornado_fetcher import Fetcher

fetcher=Fetcher(
    user_agent='phantomjs',
    phantomjs_proxy='http://192.168.7.111:9999',
    poolsize=10,
    async=False
    )

print fetcher.phantomjs_fetch('www.baidu.com')