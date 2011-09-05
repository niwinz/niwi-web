# -*- coding: utf-8 -*-

from django.views.decorators.cache import cache_page
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext, loader
from django.contrib import messages

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from pygments.styles import get_style_by_name

from niwi.models import *
from niwi.views.generic import GenericView

from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger("niwi")

class HomePageView(GenericView):
    template_name = 'niwi/index.html'

    def get(self, request):
        context = {
            'posts': Post.objects.filter(status='public').order_by('-modified_date')[:3],
        }
        try:
            config = Config.objects.get()
            context['homepage'] = Page.objects.get(pk=config.core_homepage)
        except (Page.DoesNotExist, Config.DoesNotExist):
            context['homepage'] = None
        return self.render_to_response(self.template_name, context)
        

class PostListView(GenericView):
    def get(self, request, year=None):
        if not year:
            posts = Post.objects.filter(status='public').order_by('-created_date')[:20]
        else:
            posts = Post.objects.filter(created_date__year=year, status='public').order_by('-created_date')
        
        years = [x.year for x in Post.objects.filter(status='public').dates('created_date','year')]
        context = {'posts': posts, 'years': years}
        return self.render_to_response("niwi/post_list.html", context)


import itertools

class BookmarkListView(GenericView):
    def get(self, request, year=None):
        if not year:
            bookmarks = Bookmark.objects.filter(public=True).order_by('-created_date')[:25]
        else:
            bookmarks = Bookmark.objects.filter(public=True, created_date__year=year).order_by('-created_date')

        years = [x.year for x in Bookmark.objects.filter(public=True).dates('created_date','year')]
        months = list(bookmarks.dates('created_date', 'month'))
        months.reverse()

        month_result = []
        for month in months:
            month_result.append(Bookmark.objects.filter(
                created_date__year=month.year,
                created_date__month=month.month,
            ).order_by('-created_date'))

        result = itertools.izip(months, month_result)
        context = {'bookmarks': bookmarks, 'months': months, 'years': years, 'bresult':result}
        return self.render_to_response("niwi/bookmark_list.html", context)


class PageView(GenericView):
    def get(self, request, slug):
        page = get_object_or_404(Page, slug=slug)
        context = {'object':page}
        return self.render_to_response("niwi/page_detail.html", context)
        

class PostView(GenericView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {'object':post}
        return self.render_to_response("niwi/post_detail.html", context)


class BookmarkView(GenericView):
    def get(self, request, slug):
        bookmark = get_object_or_404(Bookmark, slug=slug)
        return HttpResponseRedirect(bookmark.url)


class LangChangeView(View):
    def post(self, request, *args, **kwargs):
        if request.POST['lang'] and len(request.POST['lang']) <= 10:
            request.session['django_language'] = request.POST['lang']
            return HttpResponse('ok', mimetype="text/plain")
        else:
            return HttpResponse('error', mimetype='text/plain')

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(LangChangeView, self).dispatch(*args, **kwargs)


class Robots(TemplateView):
    template_name = "utils/robots.txt"

class Sitemap(TemplateView):
    template_name = "utils/sitemap.xml"
