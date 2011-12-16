# -*- coding: utf-8 -*-

import djcelery

BROKER_BACKEND = 'redis'
BROKER_HOST = "localhost"
BROKER_PORT = 6379
BROKER_VHOST = "0"

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

CELERY_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_DISABLE_RATE_LIMITS = True

CELERY_IMPORTS = ("niwi_apps.twitter_filter",)
CELERYD_MAX_TASKS_PER_CHILD = 1000

#from datetime import timedelta
#
#CELERYBEAT_SCHEDULE = {
#    "runs-every-30-seconds": {
#        "task": "filter-twitter-links",
#        "schedule": timedelta(seconds=30),
#    }
#}
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

INSTALLED_APPS += ['djcelery']

djcelery.setup_loader()
