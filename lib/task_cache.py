class TaskCache(object):
    """docstring for TaskCache"""
    cache = []

    def __init__(self, arg):
        self.arg = arg

    @classmethod
    def get(cls):
        if len(cls.cache) > 0:
            return cls.cache.pop()
        else:
            return None

    @classmethod
    def push(cls, url):
        cls.cache.append(url)
        pass

    @classmethod
    def is_empty(cls):
        if len(cls.cache) == 0:
            return True
        else:
            return False
