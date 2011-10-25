# -*- coding: utf-8 -*-

from django.core.cache import cache
import requests
import re

RX = re.compile(r'\s*<title>(.+)</title>\s*', flags=re.U+re.I)

class Singleton(type):
    """ Singleton metaclass. """

    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance


def get_url_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        pos = RX.findall(response.content)
        if len(pos) > 0:
            return pos[0], url
    
    return url, url



def cacheable(cache_key, timeout=3600):
    def paramed_decorator(func):
        def decorated(self, *args, **kwargs):
            key = cache_key % self.__dict__
            res = cache.get(key)
            if res == None:
                res = func(self, *args, **kwargs)
                cache.set(key, res, timeout)
            return res
        decorated.__doc__ = func.__doc__
        decorated.__dict__ = func.__dict__
        return decorated 
    return paramed_decorator
