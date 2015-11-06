#coding:utf-8
import md5
import redis

class TaskCache(object):
    """docstring for TaskCache"""
    cache = redis.Redis(db = 0)

    def __init__(self, arg):
        self.arg = arg

    @classmethod
    def get(cls):
        key_size = cls.cache.dbsize()
        if key_size > 0:
            key = cls.cache.randomkey()
            value = cls.cache.get(key)
            cls.cache.delete(key)
            return value
        else:
            return None

    @classmethod
    def push(cls, url):
        m1 = md5.new()
        m1.update(url)
        md5_value = m1.hexdigest()
        if cls.cache.exists(md5_value):
            pass
        else:
            cls.cache.set(md5_value, url)
            pass

    @classmethod
    def is_empty(cls):
        key_size = cls.cache.dbsize()
        if key_size == 0:
            return True
        else:
            return False
