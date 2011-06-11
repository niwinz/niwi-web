# -*- coding: utf-8 -*-

from django.conf import settings

def main(request):
    request.session['django_language'] = 'es'
    context_extra = dict(
        debug=settings.DEBUG,
        current_url = request.META.get('PATH_INFO'),
        full_host_url = settings.HOST + request.META.get('PATH_INFO'),
        fcbk_admin = settings.FCBK_ADMIN,
        fcbk_app_id = settings.FCBK_APP_ID,
        host = settings.HOST,
    )
    context_extra['full_current_url'] = context_extra['current_url']
    if request.META.get("QUERY_STRING"):
        context_extra['full_current_url'] += "?%s" % (request.META.get("QUERY_STRING"))
    return context_extra
