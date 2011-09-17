# -*- coding: utf-8 -*-

from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.conf import settings
import os

class GenericView(View):
    template_theme = settings.TEMPLATES_THEME

    def render_to_response(self, template_name, context, **kwargs):
        template = os.path.join(self.template_theme, template_name)
        return render_to_response(template, context, 
            context_instance=RequestContext(self.request), **kwargs)

    def msginfo(self, message):
        message.info(self.request, message)

    def msgerror(self, message):
        message.error(self.request, message)

    def dispatch(self, *args, **kwargs):
        self.head = self.get
        return super(GenericView, self).dispatch(*args, **kwargs)
