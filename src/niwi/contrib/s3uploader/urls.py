# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from .views import (
    UploaderView,
    UploaderFileView,
    UploaderDeleteFile,
)

urlpatterns = patterns('',
    url(r'^$', UploaderView.as_view(), name='home'),
    url(r'^(?P<id>\d+)/$', UploaderFileView.as_view(), name='file'),
    url(r'^(?P<id>\d+)/delete/$', UploaderDeleteFile.as_view(), name='delete-file'),
)


