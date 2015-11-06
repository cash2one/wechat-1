#coding:utf-8
import logging
import logging.handlers

LOG_FILE = 'development.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

class Log(object):
    """docstring for Log"""
    def __init__(self, class_name):
        self.class_name = class_name
        self.logger = logging.getLogger(self.class_name)
        self.logger.addHandler(handler)

    def info(sefl, message):
        sefl.logger.info(message)