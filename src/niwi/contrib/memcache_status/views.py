# -*- coding: utf-8 -*-

from django.views.generic import View
from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.conf import settings

class MemcacheStatusView(View):
    template_name = "memcache_simple_status.html"

    def get(self, request, *args, **kwargs):
        try:
            import memcache
        except ImportError:
            return HttpResponseNotFound()

        if not request.user.is_authenticated() and request.user.is_staff:
            return HttpResponseForbidden()

        if settings.CACHES['default']['BACKEND'] != 'django.core.cache.backends.memcached.MemcachedCache':
            return HttpResponseNotFound()

        context = {'stats': self.make_stats()}
        return self.render_to_response(context)

    def make_stats(self):
        cache_location =  settings.CACHES['default']['LOCATION']
        if not isinstance(cache_location, list):
            cache_location = [cache_location]
        
        import memcache
        mc = memcache.Client(cache_location, debug=0)
        return dict(mc.get_stats())

    def render_to_response(self, context):
        return render_to_response(self.template_name, context, mimetype="text/html")
