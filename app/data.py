import warnings
import os

import redis
from redis.exceptions import ConnectionError
import json


class RedisWrapper(object):
    """
    provides a uniform API for both redis client
    and python dictionary;
    falls back on python dict if redis is down.
    """
    def __init__(self, use_dict=False):

        if use_dict:
            r = {}
            self.type = 'dict'
        else:
            r = redis.Redis()
            try:
                r.ping()
                self.type = 'redis'
            except ConnectionError:
                r = {}
                msg = 'Cannot connect to redis server; using dict instead. '
                msg += 'If not testing, this will cause major slowdowns.'
                warnings.warn(msg)
                self.type = 'dict'
        self.data = r

    def __len__(self):
        if self.type == 'dict':
            return len(self.data)
        elif self.type == 'redis':
            return self.data.dbsize()

    def set(self, key, value):
        if self.type == 'dict':
            self.data[key] = value
        elif self.type == 'redis':
            self.data.set(key, value)

    def get(self, key, default=None):
        if self.type == 'dict':
            return self.data.get(key, default)
        elif self.type == 'redis':
            result = self.data.get(key)
            if result is None:
                result = default
            if isinstance(result, bytes):
                result = result.decode()
            return result

    def delete(self, key):
        """remove key from index"""
        if self.type == 'dict':
            try:
                del self.data[key]
            except KeyError:
                pass
        elif self.type == 'redis':
            self.data.delete(key)


def load_results_data(data_path='./results.json'):
    """
    Reads results data and stores in redis cache.
    Falls back on python dict if redis unavailable.
    input:
        data_path (string): path to results json file
    output:
        Returns RedisWrapper instance.
    """
    r = RedisWrapper()
    if len(r) == 0:
        with open(data_path, 'rb') as f:
            for line in f.readlines():
                data = line
                data = json.loads(data)
                key = data['search_key']
                res = data['results']
                r.set(key, str(res))
    return r
