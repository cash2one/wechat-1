#coding:utf-8
import logging
import sys
sys.path.append("..")
import config

class Log(object):
    """docstring for Log"""
    def __init__(self, class_name):
        self.class_name = class_name
        self.logger = logging.getLogger(self.class_name)
        self.logger.addHandler(config.handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
