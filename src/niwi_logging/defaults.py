# -*- coding: utf-8 -*-
import os.path
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'en-us'
SECRET_KEY = 'sp*ot9o#uki#3=wz#424)zivrtx11@!&h#k1=g9f_h$9(#%cyh'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'niwi_logging.middleware.AuthMiddleware',
)

ROOT_URLCONF = 'niwi_logging.urls'

INSTALLED_APPS = (
    'niwi_logging',
)

LOGGING = {}
