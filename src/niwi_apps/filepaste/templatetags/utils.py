# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.template import loader

from niwi.utils import Singleton
from niwi.models import Config

register = template.Library()

class HomePageNode(template.Node):
    def __init__(self):
        self.homepage = Config.objects.home_page

    def render_filepaste(self, context):
        return u""

    def render_page(self, context):
        from niwi.models import Page
        try:
            page = Page.objects.get(slug=self.homepage)
        except Page.DoesNotExist:
            return mark_safe(u"")
    
        context = {
            'hpage':page.content,
            'markup':page.markup
        }
        template_name = "%s/utils/homepage.html" % (settings.TEMPLATES_THEME)
        return mark_safe(loader.render_to_string(template_name, context))

    def render(self, context):
        if self.homepage == 'filepaste':
            return self.render_filepaste(context)
        else:
            return self.render_page(context)


@register.tag(name="homepage")
def homepage(parser, token):
    return HomePageNode()

