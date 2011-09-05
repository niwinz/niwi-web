# -*- coding: utf-8 -*-

from django.conf import settings

def main(request):
    context_extra = dict(
        debug=settings.DEBUG,
        current_url = request.META.get('PATH_INFO'),
        full_host_url = settings.HOST + request.META.get('PATH_INFO'),
        fcbk_admin = settings.FCBK_ADMIN,
        fcbk_app_id = settings.FCBK_APP_ID,
        host = settings.HOST,
        page_default_logo_url = settings.PAGE_DEFAULT_LOGO_URL,
        page_default_description = settings.PAGE_DEFAULT_DESCRIPTION,
        page_default_keyworkds = settings.PAGE_DEFAULT_KEYWORKDS,
        page_default_title = settings.PAGE_DEFAULT_TITLE
    )
    context_extra['full_current_url'] = context_extra['current_url']
    if request.META.get("QUERY_STRING"):
        context_extra['full_current_url'] += "?%s" % (request.META.get("QUERY_STRING"))
    return context_extra
