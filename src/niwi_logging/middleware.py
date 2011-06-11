# -*- coding: utf-8 -*-
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
import re

from pprint import pprint

class AuthMiddleware(object):
    def process_request(self, request):
        if "username" not in request.POST:
            return HttpResponseForbidden()

        if "password" not in request.POST:
            return HttpResponseForbidden()

        return None
