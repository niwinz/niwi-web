# -*- coding: utf-8 -*-

import os
import os.path
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.local'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
