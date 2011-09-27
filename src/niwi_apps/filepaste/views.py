# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404
from niwi.views.generic import GenericView
from niwi_apps.filepaste.models import WebFile
import os.path

class WebFileDownload(GenericView):
    template_name = "filepaste_item.html"
    def get(self, request, slug):
        wfile = get_object_or_404(WebFile, slug=slug)
        if not wfile.password:
            response = HttpResponse(mimetype="application/octet-stream")
            response['X-Accel-Redirect'] = wfile.attached_file.url
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                os.path.basename(wfile.attached_file.name)
            print wfile.attached_file.url
            return response

        else:
            return self.render_to_response(self.template_name)
