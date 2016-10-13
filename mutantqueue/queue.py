import redis


class PriorityQueue:
    LUA_ZPOP = """
    local result = redis.call('ZRANGE', KEYS[1], -1, -1)
    if result then redis.call('ZREMRANGEBYRANK', KEYS[1], -1, -1) end
    return result"""

    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.zpop = self.redis.register_script(self.LUA_ZPOP)
        self.key = 'priority_queue'

    def insert(self, *args, **kwargs):
        return self.redis.zadd(self.key, *args, **kwargs)

    def pop(self):
        element = self.zpop(keys=[self.key])
        return element[0] if hasattr(element, '__iter__') else element

    def remove(self, *elements):
        return self.redis.zrem(self.key, *elements)

    @property
    def size(self):
        return self.redis.zcard(self.key)
