# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from niwi.photo.views import *

urlpatterns = patterns('',
    url(r'^$', PhotoHome.as_view(), name='show-home'),
    url(r'^albums/$', AlbumsView.as_view(), name='show-albums'),
    url(r'^album/(?P<aslug>[\w\d\-]+)/$', AlbumPhotosView.as_view(), name='show-album'),
    url(r'^album/(?P<aslug>[\w\d\-]+)/photo/(?P<pslug>[\w\d\-]+)/$', PhotoView.as_view(), name='show-photo'),
)
