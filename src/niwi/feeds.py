# -*- coding: utf-8 -*-
# Thanks to Vladimir Epifanov <voldmar@voldmar.ru>

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.markup.templatetags.markup import markdown

from .models import Post, Page

class LatestPostsFeed(Feed):
    feed_type = Atom1Feed
    title = 'Ultimas entradas en Niwi.Be'
    link = '/'

    def items(self):
        return Post.objects.exclude(status="public").order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.content)
