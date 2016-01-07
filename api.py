#coding:utf-8
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
import config

define("port", default = config.SERVER_PORT, help = "run port", type = int)
define("mysql_host", default = config.MYSQL_HOST)
define("mysql_database", default = config.MYSQL_DATABASE)
define("mysql_user", default = config.MYSQL_USER)
define("mysql_password", default = config.MYSQL_PASSWORD)

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
        if REDIS_CACHE.is_empty():
            response_body = '<script type="text/javascript">location.href="http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=%s#wechat_redirect"</script>'
            db = self.application.db
            last_official_account = db.get("SELECT * FROM official_account ORDER BY last_update_time ASC LIMIT 1")

            if last_official_account != None:
                official_account = last_official_account.get('wechat_code')
                official_account_id = last_official_account.get('id')
                if official_account_id is not None:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    db.execute("UPDATE official_account SET last_update_time = \'%s\' WHERE id = %d" % (now, official_account_id))
                self.write(response_body % official_account)
            else:
                self.write('empty')
        else:
            article_url = REDIS_CACHE.get_random()
            if article_url != None:
                self.write('<script type="text/javascript">location.href="%s"</script>' % article_url)
            else:
                self.write('empty')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())

    print "Start server on: %d" % options.port
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
