# -*- coding: utf-8 -*-

from .common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

USE_ETAGS=True

#SESSION_ENGINE='django.contrib.sessions.backends.db'
SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 1209600 # (2 weeks)


MIDDLEWARE_CLASSES += [
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
]
