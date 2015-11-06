#coding:utf-8
import md5
import redis

class TaskCache(object):
    """docstring for TaskCache"""

    def __init__(self, host = '127.0.0.1', port = 6309, db = 0):
        self.cache = redis.Redis(host = host, port = port, db = db)

    def get(self):
        key_size = self.cache.dbsize()
        if key_size > 0:
            key = self.cache.randomkey()
            value = self.cache.get(key)
            self.cache.delete(key)
            return value
        else:
            return None

    def push(self):
        m1 = md5.new()
        m1.update(url)
        md5_value = m1.hexdigest()
        if self.cache.exists(md5_value):
            pass
        else:
            self.cache.set(md5_value, url)
            pass

    def is_empty(self):
        key_size = self.cache.dbsize()
        if key_size == 0:
            return True
        else:
            return False