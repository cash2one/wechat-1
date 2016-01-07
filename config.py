#coding:utf-8
import os
import MySQLdb
from skylark import Database

ROOT_PATH = os.getcwd()

LOG_FILE = ROOT_PATH + '/log/development.log'

SERVER_PORT = 8888

MYSQL_HOST = "127.0.0.1:3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DATABASE = "wechat"

Database.set_dbapi(MySQLdb)
Database.config(user = MYSQL_USER, passwd = MYSQL_PASSWORD, db = MYSQL_DATABASE)
