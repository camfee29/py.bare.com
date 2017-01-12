import memcache
import configparser
import os.path

class MemcacheDB:
    def __init__(self):
        self.__config(['memcache'])
    def __config(self, section):
        conf = configparser.ConfigParser()
        conf.read(os.path.split(os.path.realpath(__file__))[0] + "/../Config/db.conf")
        self.__host_port = []
        for val in section:
            self.__host_port.append(conf.get(val, 'host_port'))
        self._connect()
    def _connect(self):
        self._memcache = memcache.Client(self.__host_port, debug = 0)
        return self._memcache
    def selectConfig(self, section):
        self.__config(section)
        return self
    # keys为dict时val表示前缀
    def set(self, keys, val = '', time = 0, min_compress_len = 0):
        if isinstance(keys, dict):
            return self._memcache.set_multi(keys, time, val, min_compress_len)
        else:
            return self._memcache.set(keys, val, time, min_compress_len)
    def get(self, keys, key_prefix = ''):
        if isinstance(keys, list):
            return self._memcache.get_multi(keys, key_prefix)
        else:
            return self._memcache.get(keys)
    def delete(self, key):
        return self._memcache.delete(key)
    def incr(self, key, delta = 1):
        return self._memcache.incr(key, delta)
    def decr(self, key, delta = 1):
        return self._memcache.decr(key, delta)
