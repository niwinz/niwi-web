# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404

from niwi.views.generic import GenericView
from niwi_apps.filepaste.models import WebFile
from niwi_apps.filepaste.forms import UploadForm
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
            return response

        else:
            return self.render_to_response(self.template_name)


class WebFileUpload(GenericView):
    template_name = "filepaste_upload.html"

    def get(self, request):
        form = UploadForm()
        return self.render_to_response(self.template_name, {'form':form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            wfile = form.save()
            return HttpResponseRedirect(reverse("web:show-home"))

        return self.render_to_response(self.template_name, {'form':form})
