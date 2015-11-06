import os.path
import torndb
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.web
import datetime

from lib.task_cache import TaskCache
from lib.log import Log
from tornado.options import define, options

define("port", default = 8888, help="run port", type=int)
define("mysql_host", default = "127.0.0.1:3306")
define("mysql_database", default="wechat")
define("mysql_user", default="root")
define("mysql_password", default="123456")

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
REDIS_CACHE = TaskCache(db = 1)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/get/task", Task)
        ]
        settings = dict(
            template_path = TEMPLATE_PATH,
            static_path = STATIC_PATH,
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        print "Database connection"
        self.db = torndb.Connection(
            host = options.mysql_host,
            database = options.mysql_database,
            user = options.mysql_user,
            password = options.mysql_password
        )


class Task(tornado.web.RequestHandler):
    def get(self):
        response_body = '<script type="text/javascript">location.href="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s#wechat_redirect"</script>'
        # http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==#wechat_webview_type=1&wechat_redirect
        # http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==#wechat_redirect
        # http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==&uin=NTE1MzA0MDAw&key=b410d3164f5f798e28810fbab3aa65786404571bdf138523122da8508b8eb1f6c95b1aab07a4632aa87818bb9c0ed004&devicetype=android-22&version=26030531&lang=en&nettype=WIFI&pass_ticket=9DETPZPf3uBJKnvyUxvGV4cYtz%2FHEJ%2BASCcLW9kzfxyLekagwBewH3sTp9ZD2ktS
        # http://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5ODIyMTE0MA==&appmsgid=10000382&itemidx=1#wechat_redirect
        # http://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5ODIyMTE0MA==&appmsgid=10000382#wechat_redirect
        # self.write('<script type="text/javascript">location.href="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==#wechat_redirect"</script>')

        if REDIS_CACHE.is_empty():
            db = self.application.db
            last_official_account = db.get("SELECT * FROM official_account ORDER BY last_update_time ASC LIMIT 1")

            if last_official_account != None:
                official_account = last_official_account.get('wechat_code')
                official_account_id = last_official_account.get('id')
                if official_account_id is not None:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.execute("UPDATE official_account SET last_update_time = \'%s\' WHERE id = %d" % now, official_account_id)
                self.write(response_body % official_account)
            else:
                self.write('<script type="text/javascript">location.href="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==#wechat_redirect"</script>')
        else:
            self.write('<script type="text/javascript">location.href="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MzIwNzA1MTg0OQ==#wechat_redirect"</script>')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())

    print "Start server on: %d" % options.port
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
