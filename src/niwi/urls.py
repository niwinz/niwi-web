# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^memcached/', include('niwi.contrib.memcache_status.urls', namespace='memcachestatus')),
    #url(r'^s3uploader/', include('niwi.contrib.s3uploader.urls', namespace='s3uploader')),
)

from django.views.generic import RedirectView
from niwi.web.views.main import Sitemap, Robots

urlpatterns += patterns('',
    url(r'^', include('niwi.web.urls', namespace="web")),
    url(r'^photo/', include('niwi.photo.urls', namespace='photo')),
    #url(r'^filepaste/', include('niwi_apps.filepaste.urls', namespace='filepaste')),
    url(r'^robots.txt$', Robots.as_view(), name='robots'),
    url(r'^sitemap.xml$', Sitemap.as_view(), name='sitemap'),
)

# Static files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('', 
            (r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT})
        )
