import json

from redis.asyncio import ConnectionPool, Redis


class Cache:
    def __init__(self):
        self.conn_pool = ConnectionPool(host='redis', port=6379)
    
    async def get(self, key):
        r = Redis(connection_pool=self.conn_pool)
        encoded_val = await r.get(key)
        value = json.loads(encoded_val.decode("utf-8")) if encoded_val else None
        return value
    
    async def set(self, key, value):
        r = Redis(connection_pool=self.conn_pool)
        await r.set(key, json.dumps(value))
