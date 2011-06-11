# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^memcached/', include('niwi.contrib.memcache_status.urls', namespace='memcachestatus')),
    #url(r'^s3uploader/', include('niwi.contrib.s3uploader.urls', namespace='s3uploader')),
)

from django.views.generic import RedirectView

urlpatterns += patterns('',
    #url(r'^$', RedirectView.as_view(url="/w/"), name="root"),
    url(r'^', include('niwi.urls', namespace="web")),
    url(r'^robots.txt$', 'niwi.views.robots', name='robots'),
    url(r'^sitemap.xml$', 'niwi.views.sitemap', name='sitemap'),
)

# Static files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

