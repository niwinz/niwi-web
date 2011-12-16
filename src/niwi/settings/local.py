# -*- coding: utf-8 -*-
from .development import *
#from .celery import *

# AMAZON
AWS_ACCESS_KEY = 'AKIAJHJGSRFNJVMYWUXA'
AWS_SECRET_KEY = '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'

TEMPLATES_THEME='niwi'

PAGE_DEFAULT_LOGO_URL='http://www.niwi.be/static/logo.png'
PAGE_DEFAULT_DESCRIPTION='My personal blog, dedicated to my small contribution to the opensource world.'
PAGE_DEFAULT_KEYWORKDS='niwi, niwi.be, projects, links, photos, opensource, bsd, freebsd, linux'
PAGE_DEFAULT_TITLE='Niwi.Be'

FCBK_APP_ID = '217309748280027'
FCBK_APP_SECRET = '3ae72c5d9743dbbab93a36bd2f502b8b'
FCBK_APP_API = 'a4628019b87fd9c2fa9bec01d8ae8f54'
FCBK_ADMIN = '726587823'

# Use my self backend
#import sys
#sys.path.insert(0, '/home/niwi/devel/django-orm')

#DATABASES = {
#    'default': {
#        #'ENGINE': 'django.db.backends.postgresql_psycopg2', 
#        'ENGINE': 'django_orm.backends.postgresql_psycopg2',
#
#        'NAME': 'niwiweb',         
#        'USER': 'niwi',            
#        'PASSWORD': '123123',      
#        'HOST': 'localhost',       
#        'PORT': '5432',             
#    }, 
#}

#DATABASES = {
#    'default': {
#        #'ENGINE': 'django.db.backends.postgresql_psycopg2', 
#        #'ENGINE': 'django_orm.backends.postgresql_psycopg2',
#        #'ENGINE': 'django_orm.backends.mysql',
#        #'ENGINE': 'django.db.backends.mysql',
#        #'ENGINE': 'django_orm.backends.sqlite3',
#        'NAME': '/tmp/niwiweb',   
#        'USER': 'root',      
#        'PASSWORD': '',      
#        'HOST': '',          
#        'PORT': '',          
#    }, 
#}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
     }
}

#CACHES = {
#    'default': {
#        'BACKEND': 'redis_cache.cache.RedisCache',
#        'LOCATION': '127.0.0.1:6379',
#        'OPTIONS': { 
#            'DB': 2,
#        },
#    },
#    'ormcache': {
#        'BACKEND': 'redis_cache.cache.RedisCache',
#        'LOCATION': '127.0.0.1:6379',
#        'OPTIONS': { 
#            'DB': 1,
#        },
#    },
#}

#DEVSERVER_MODULES += [
#    'devserver.modules.sql.SQLRealTimeModule',
#]
