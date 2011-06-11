# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
import os.path, sys

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Andrei Antoukh', 'niwi@niwi.be'),
)

MANAGERS = ADMINS

FCBK_APP_ID = ''
FCBK_APP_SECRET = ''
FCBK_APP_API = ''
FCBK_ADMIN = ''

SEND_BROKEN_LINK_EMAILS = False
IGNORABLE_404_ENDS = ('.php', '.cgi')
IGNORABLE_404_STARTS = ('/phpmyadmin/',)
DEFAULT_CONTENT_TYPE = "text/html"
HOST = 'http://www.niwi.be'

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'database.sqlite'),
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
     }
}

# ETAGS Feature for good cache. (true only for production)
USE_ETAGS=True

#SESSION BACKEND
SESSION_ENGINE='django.contrib.sessions.backends.db'
#SESSION_ENGINE='django.contrib.sessions.backends.cache'
#SESSION_EXPIRE_AT_BROWSER_CLOSE = False
#SESSION_SAVE_EVERY_REQUEST = False
#SESSION_COOKIE_AGE = 1209600 # (2 weeks)


# MAIL OPTIONS
#EMAIL_USE_TLS = False
#EMAIL_HOST = 'localhost'
#EMAIL_HOST_USER = 'user'
#EMAIL_HOST_PASSWORD = 'password'
#EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "niwi@niwi.be"

# Message System
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
#MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'es'
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

SECRET_KEY = '^xur70b9%*5vl+v&t=8v8bs5)5%0em^-oyzuj6#*r*0vcjdy4)'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'niwi.middleware.FacebookMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.contrib.messages.context_processors.messages",
    "niwi.context.main",
)


ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    #os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'niwi',
    'niwi.paste',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(module)s:%(process)d:%(message)s'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends':{
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'niwi':{
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
