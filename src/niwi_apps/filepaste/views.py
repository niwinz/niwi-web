# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404

from niwi.niwi.views.generic import GenericView
from niwi.niwi_apps.filepaste.models import WebFile
from niwi.niwi_apps.filepaste.forms import UploadForm, DownloadForm
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
            
        form = DownloadForm(wfile=wfile)
        return self.render_to_response(self.template_name,
            {'form':form, 'file':wfile})

    def post(self, request, slug):
        wfile = get_object_or_404(WebFile, slug=slug)
        form = DownloadForm(request.POST, wfile=wfile)
        if form.is_valid():
            response = HttpResponse(mimetype="application/octet-stream")
            response['X-Accel-Redirect'] = wfile.attached_file.url
            response['Content-Disposition'] = 'attachment; filename=%s' % \
                os.path.basename(wfile.attached_file.name)
            return response
        
        return self.render_to_response(self.template_name,
            {'form': form, 'file':wfile})

class WebFileUpload(GenericView):
    template_name = "filepaste_upload.html"

    def get(self, request):
        form = UploadForm()
        return self.render_to_response(self.template_name, {'form':form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            wfile = form.save(commit=False)
            if form.cleaned_data['password']:
                wfile.set_password(form.cleaned_data['password'])

            wfile.save()
            return HttpResponseRedirect(reverse("web:show-home"))

        return self.render_to_response(self.template_name, {'form':form})
