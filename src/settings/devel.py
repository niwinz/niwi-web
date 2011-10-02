# -*- coding: utf-8 -*-

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

USE_ETAGS=False

TEMPLATE_CONTEXT_PROCESSORS += [
    "django.core.context_processors.debug",
]

LOGGING['handlers']['query_fileout'] = {
    'level':'DEBUG',
    'class':'logging.FileHandler',
    'filename': os.path.join(LOGS_PATH, 'querys.log'),
}

LOGGING['loggers']['django.db.backends']['handlers'] = ['query_fileout']
