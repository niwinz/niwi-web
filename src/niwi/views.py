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


class CacheMixIn(object):
    """ Class for generic cache decorator. """
    template_name = None
    
    #@method_decorator(cache_page(40)) 
    def dispatch(self, *args, **kwargs):
        self.head = self.get
        return super(CacheMixIn, self).dispatch(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        return render_to_response(self.get_template_names(), context,
            context_instance = RequestContext(self.request), **response_kwargs)
    
class ObjectListMixIn(ListView):
    """ Class for generic settings for all object list. """
    allow_empty = True
    paginate_by = 20


class HomePageView(CacheMixIn, TemplateView):
    template_name = 'niwi/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)

        try:
            config = Config.objects.get(path='core.homepage')
            context['homepage'] = Page.objects.get(uuid=config.value)

        except (Page.DoesNotExist, Config.DoesNotExist):
            context['homepage'] = None
        
        return context


class PageView(CacheMixIn, DetailView):
    queryset = Page.objects.all()
    context_object_name = "page"


class PostsView(CacheMixIn, ObjectListMixIn):
    queryset = Post.objects.filter(status='public').order_by('-created_date')


class LinksView(CacheMixIn, ObjectListMixIn):
    queryset = Link.objects.exclude(public=False).order_by('-created_date')


class ProjectsView(CacheMixIn, ListView):
    context_object_name = 'projects'
    queryset = Project.objects.all().order_by('title')


class PostView(CacheMixIn, DetailView):
    queryset = Post.objects.all()


class LinkView(CacheMixIn, DetailView):
    queryset = Link.objects.exclude(public=False)

    def render_to_response(self, context, **kwargs):
        linkobj = self.get_object()
        return HttpResponseRedirect(linkobj.url)


class ProjectView(CacheMixIn, DetailView):
    model = Project


@cache_page(7200)
def robots(request):
    return render_to_response("utils/robots.txt", {}, mimetype="text/plain")

@cache_page(60)
def sitemap(request):
    return render_to_response("utils/sitemap.xml", {}, mimetype="application/xml")
