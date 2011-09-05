# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from .feeds import *
from .views.main import *
from .views.paste import *

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='show-home'),
    url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404"),

    url(r'^posts/$', PostListView.as_view(), name='posts'),
    url(r'^posts/year/(?P<year>\d+)/$', PostListView.as_view(), name='posts'),

    url(r'^posts/feed/$', LatestPostsFeed(), name='posts-feed'),
    url(r'^post/(?P<slug>[\w\d\-]+)/$', PostView.as_view(), name='show-post'),

    url(r'^bookmarks/$', BookmarkListView.as_view(), name='bookmarks'),
    url(r'^bookmark/(?P<slug>[\w\d\-]+)/$', BookmarkView.as_view(), name='show-bookmark'),
    
    url(r'^page/(?P<slug>[\w\d\-]+)/$', PageView.as_view(), name="show-page"),
    url(r'^set/lang/$', LangChangeView.as_view(), name="set-lang"),
    
    url(r'^paste/$', PasteHomeView.as_view(), name='paste-home'),
    url(r'^paste/(?P<pasteid>\d+)/$', PasteDetailView.as_view(), name='paste-view'),
    url(r'^paste/(?P<pasteid>\d+)/raw/$', PasteDetailRawView.as_view(), name='paste-view-raw'),
)


