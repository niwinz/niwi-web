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
            config_object = Config.objects.get()
            self.analytics_code = config_object.google_analytics_code
            self.analytics_domain = config_object.google_analytics_domain
            self.enabled = True

        except Config.DoesNotExist:
            self.enabled = False

    def render(self, context):
        if self.enabled:
            context.update({'code': self.analytics_code, 'domain': self.analytics_domain})
            return template.loader.render_to_string("niwi/utils/analytics.html", context)
        else:
            return ''


@register.tag(name="analytics")
def analytics_tag(parser, token):
    return AnalyticsNode()


class ShowPageNode(template.Node):
    """ Show and render page. """

    def __init__(self, pagename):
        self.pagename = pagename

    def render(self, context):
        from niwi.models import Page
        try:
            page = Page.objects.get(slug=self.pagename)
        except Page.DoesNotExist:
            return mark_safe('')
        
        t = template.Template(page.content)
        result = t.render(context)
        return mark_safe(result)


@register.tag(name="show_page")
def show_page(parser, token):
    try:
        tag_name, page_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

    if not (page_name[0] == page_name[-1] and page_name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return ShowPageNode(page_name[1:-1])



@register.filter(name="parse_tags")
def parse_tags(value):
    split = None if "," not in value else ","
    tags = [tag.strip() for tag in value.split(split)]
    tags_html = ['<a href="%s">%s</a>' % ('', tagname) for tagname in tags]
    return mark_safe(", ".join(tags_html))
