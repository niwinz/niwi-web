# -*- coding: utf-8 -*-
# Thanks to Vladimir Epifanov <voldmar@voldmar.ru>

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.markup.templatetags.markup import markdown
from django.utils.translation import ugettext_lazy as _

from niwi.web.models import Post, Page

class LatestPostsFeed(Feed):
    feed_type = Atom1Feed
    title = _(u'Ultimas entradas')
    link = '/'

    def items(self):
        return Post.objects.filter(status="public").order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        # TODO: fix this
        return markdown(item.content)
