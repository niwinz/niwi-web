# -*- coding: utf-8 -*-

from django.views.decorators.cache import cache_page
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, ListView

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib import messages

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.styles import get_style_by_name

from niwi.models import *

from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger("niwi")


class ResponseMixIn(object):
    """ Class for generic cache decorator. """
    template_name = None
    
    def dispatch(self, *args, **kwargs):
        self.head = self.get
        return super(ResponseMixIn, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return render_to_response(self.get_template_names(), context,
            context_instance = RequestContext(self.request), **response_kwargs)
    

class ObjectListMixIn(ListView):
    """ Class for generic settings for all object list. """
    allow_empty = True
    paginate_by = 20


class HomePageView(ResponseMixIn, TemplateView):
    template_name = 'niwi/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['posts'] = Post.objects.order_by('-modified_date')[:10]

        try:
            config = Config.objects.get(path='core.homepage')
            context['homepage'] = Page.objects.get(uuid=config.value)

        except (Page.DoesNotExist, Config.DoesNotExist):
            context['homepage'] = None
        
        return context


class DocumentView(ResponseMixIn, DetailView):
    template_name = 'niwi/page_detail.html'
    queryset = Document.objects.all()
    context_object_name = "page"


class PageView(ResponseMixIn, DetailView):
    queryset = Page.objects.all()
    context_object_name = "page"


class PostsView(ResponseMixIn, ObjectListMixIn):
    queryset = Post.objects.filter(status='public').order_by('-created_date')


class LinksView(ResponseMixIn, ObjectListMixIn):
    queryset = Link.objects.exclude(public=False).order_by('-created_date')


class PostView(ResponseMixIn, DetailView):
    queryset = Post.objects.all()


class LinkView(ResponseMixIn, DetailView):
    queryset = Link.objects.exclude(public=False)

    def render_to_response(self, context, **kwargs):
        linkobj = self.get_object()
        return HttpResponseRedirect(linkobj.url)



class Robots(TemplateView):
    template_name = "utils/robots.txt"

class Sitemap(TemplateView):
    template_name = "utils/sitemap.xml"

#def robots(request):
#    return render_to_response("utils/robots.txt", {}, mimetype="text/plain")
#
#def sitemap(request):
#    return render_to_response("utils/sitemap.xml", {}, mimetype="application/xml")
