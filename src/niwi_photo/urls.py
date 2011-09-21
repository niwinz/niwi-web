# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from niwi_photo.views import *

urlpatterns = patterns('',
    url(r'^$', PhotoHome.as_view(), name='show-home'),
)
