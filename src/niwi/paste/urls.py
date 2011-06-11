from django.conf.urls.defaults import *

urlpatterns = patterns('niwi.paste.views',
    url(r'^$', 'paste', name='paste-home'),
    url(r'^(?P<pasteid>\d+)/$', 'paste_view', name='paste-view'),
    url(r'^(?P<pasteid>\d+)/raw/$', 'paste_view_raw', name='paste-view-raw'),
)
