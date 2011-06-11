# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from .feeds import LatestPostsFeed 
from .views import DocumentView, PageView,  HomePageView, \
    PostsView, PostView, LinksView, LinkView 


urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='show-home'),
    url(r'^404/$', TemplateView.as_view(template_name="404.html"), name="404"),

    url(r'^posts/$', PostsView.as_view(), name='posts'),
    url(r'^posts/feed/$', LatestPostsFeed(), name='posts-feed'),
    url(r'^post/(?P<slug>[\w\d\-]+)/$', PostView.as_view(), name='show-post'),

    url(r'^links/$', LinksView.as_view(), name='links'),
    url(r'^link/(?P<slug>[\w\d\-]+)/$', LinkView.as_view(), name='show-link'),
    
    url(r'^page/(?P<slug>[\w\d\-]+)/$', PageView.as_view(), name="show-page"),
    url(r'^doc/(?P<slug>[\w\d\-]+)/$', DocumentView.as_view(), name="show-doc"),
    
    # Old style views
    url(r'^paste/$', 'niwi.paste.views.paste', name='paste-home'),
    url(r'^paste/(?P<pasteid>\d+)/$', 'niwi.paste.views.paste_view', name='paste-view'),
    url(r'^paste/(?P<pasteid>\d+)/raw/$', 'niwi.paste.views.paste_view_raw', name='paste-view-raw'),
)


