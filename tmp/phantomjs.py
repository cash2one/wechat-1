from tornado_fetcher import Fetcher

fetcher=Fetcher(
    user_agent='phantomjs',
    phantomjs_proxy='http://localhost:12306',
    poolsize=10,
    async=False
    )

print fetcher.phantomjs_fetch(url)