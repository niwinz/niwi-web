# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^niwi-admin/', include(admin.site.urls)),
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

def mediafiles_urlpatterns():
    """
    Method for serve media files with runserver.
    """

    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]

    from django.views.static import serve
    return patterns('',
        (r'^%s(?P<path>.*)$' % _media_url, serve,
            {'document_root': settings.MEDIA_ROOT})
    )

urlpatterns += staticfiles_urlpatterns()
urlpatterns += mediafiles_urlpatterns()
