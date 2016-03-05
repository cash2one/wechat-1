#coding:utf-8
import os
import logging
import logging.handlers
from peewee import MySQLDatabase

ROOT_PATH = os.getcwd()

LOG_FILE = ROOT_PATH + '/log/development.log'

DOWNLOAD_PATH = '/mnt/sdc1/wechat/download'

SERVER_PORT = 8888

MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "wechat"

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

MYSQL_DB = MySQLDatabase(MYSQL_DATABASE, host = MYSQL_HOST, user = MYSQL_USER, \
    passwd = MYSQL_PASSWORD, charset = 'utf8')









