# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

from niwi.utils import Singleton
from niwi.models import Config

register = template.Library()

@register.filter(name="markdown")
def markdown(value, arg=''):
    try:
        from niwi.contrib.markdown2 import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in {% markdown %} filter: The Python markdown library isn't installed.")
        return force_unicode(value)
    else:
        extensions = {'code-color':{'style':'trac'}}
        return mark_safe(markdown(force_unicode(value), extras=extensions))

markdown.is_safe = True


@register.filter(name="fixname")
def correct_filename(name):
    return name.rsplit("/",1)[-1]


class AnalyticsNode(template.Node):
    """ Analytics singleton Node. """

    def __init__(self):
        self.enabled = None
        try:
            self.analytics_code = Config.objects.get(path="contrib.google.analytics.code").value
            self.analytics_domain = Config.objects.get(path="contrib.google.analytics.domain").value
            self.enabled = True
        except Config.DoesNotExist:
            self.enabled = False

    def render(self, context):
        if self.enabled:
            context.update({'code': self.analytics_code, 'domain': self.analytics_domain})
            return template.loader.render_to_string("utils/analytics.html", context)
        else:
            return ''

@register.tag(name="analytics")
def analytics_tag(parser, token):
    return AnalyticsNode()



