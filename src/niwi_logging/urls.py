# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from .views import LogHandlerView

urlpatterns = patterns('',
    url(r'^$', LogHandlerView.as_view(), name='log-server'),
)
