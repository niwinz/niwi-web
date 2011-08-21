# -*- coding: utf-8 -*-

from django.views.generic import View
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib import messages

class GenericView(View):
    def render_to_response(self, template_name, context, **kwargs):
        return render_to_response(template_name, context, 
            context_instance=RequestContext(self.request), **kwargs)

    def msginfo(self, message):
        message.info(self.request, message)

    def msgerror(self, message):
        message.error(self.request, message)

    def dispatch(self, *args, **kwargs):
        self.head = self.get
        return super(GenericView, self).dispatch(*args, **kwargs)
