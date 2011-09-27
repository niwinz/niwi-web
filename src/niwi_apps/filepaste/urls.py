# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, RedirectView

from niwi_apps.filepaste.views import *

urlpatterns = patterns('',
    url(r'^(?P<slug>[\d\w\-]+)/download/$', WebFileDownload.as_view(), name="download-wfile"),
    url(r'^upload/file/$', WebFileUpload.as_view(), name="upload-file"),
)
