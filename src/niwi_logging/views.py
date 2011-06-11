# -*- coding: utf-8 -*-
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.shortcuts import render_to_response


import logging

local_loggers = {}

class LogHandlerView(View):
    def post(self, request, *args, **kwargs):
        logger_key = u"%s_%s" % (request.POST['reference'], request.POST['name'])
        logger_val = request.POST['record']
        
        if logger_key in local_loggers:
            logger_obj = local_loggers[logger_key]
        else:
            local_loggers[logger_key] = logging.getLogger(logger_key)
            logger_obj = local_loggers[logger_key]

        logger_obj.info(logger_val)
        return HttpResponse('ok', mimetype="text/plain")
