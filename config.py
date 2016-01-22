#coding:utf-8
import os
import logging
import logging.handlers
import MySQLdb

from skylark import Database

ROOT_PATH = os.getcwd()

LOG_FILE = ROOT_PATH + '/log/development.log'

DOWNLOAD_PATH = ROOT_PATH + '/download'

SERVER_PORT = 8888

MYSQL_HOST = "127.0.0.1:3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "wechat"

LOG_FILE = 'log/development.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

Database.set_dbapi(MySQLdb)
Database.config(user = MYSQL_USER, passwd = MYSQL_PASSWORD, \
    db = MYSQL_DATABASE, charset='utf8', use_unicode = True)

