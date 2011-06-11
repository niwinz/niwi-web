from django.conf.urls.defaults import *

from .views import MemcacheStatusView

urlpatterns = patterns('',
    url(r'^stats/', MemcacheStatusView.as_view(), name="memcache-status"),
)
