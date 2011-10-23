# -*- coding: utf-8 -*-

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

USE_ETAGS=False

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

TEMPLATE_CONTEXT_PROCESSORS += [
    "django.core.context_processors.debug",
]

LOGGING['handlers']['query_fileout'] = {
    'level':'DEBUG',
    'class':'logging.FileHandler',
    'filename': os.path.join(LOGS_PATH, 'querys.log'),
}

LOGGING['loggers']['django.db.backends']['handlers'] = ['query_fileout']

SESSION_ENGINE='django.contrib.sessions.backends.db'
#SESSION_ENGINE='django.contrib.sessions.backends.cache'


INSTALLED_APPS += [
    'devserver',
]

DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    #'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)
