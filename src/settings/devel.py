# -*- coding: utf-8 -*-

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andrei Antoukh', 'niwi@niwi.be'),
)

MANAGERS = ADMINS
USE_ETAGS=False
SESSION_ENGINE='django.contrib.sessions.backends.cache'
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 1209600 # (2 weeks)


TEMPLATE_CONTEXT_PROCESSORS += [
    "django.core.context_processors.debug",
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
