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


class HomePageNode(template.Node):
    def __init__(self):
        self.homepage = Config.objects.home_page

    def render_filepaste(self, context):
        key, pageslug = None, None
        if len(self.homepage.split(",")) == 2:
            pageslug = self.homepage.split(",")[1]
            
        from niwi_apps.filepaste.models import WebFile
        context = {
            'files': WebFile.objects.filter(hidden=False),
            'pageslug': pageslug,
        }
        template_name = "%s/filepaste_page.html" % (settings.TEMPLATES_THEME)
        return mark_safe(loader.render_to_string(template_name, context))


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
        if 'filepaste' in self.homepage:
            return self.render_filepaste(context)
        else:
            return self.render_page(context)


@register.tag(name="homepage")
def homepage(parser, token):
    return HomePageNode()


class AnalyticsNode(template.Node):
    """ Analytics singleton Node. """

    def __init__(self):
        self.enabled = False
        self.analytics_code = Config.objects.google_analytics_code
        self.analytics_domain = Config.objects.google_analytics_domain

        if self.analytics_code:
            self.enabled = True

    def render(self, context):
        if self.enabled:
            context.update({'code': self.analytics_code, 'domain': self.analytics_domain})
            return template.loader.render_to_string(
                "%s/utils/analytics.html" % (settings.TEMPLATES_THEME), context)
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
        pagename = self.pagename.resolve(context)
        from niwi.models import Page
        try:
            page = Page.objects.get(slug=pagename)
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
    return ShowPageNode(parser.compile_filter(page_name))


@register.filter(name="parse_tags")
def parse_tags(value):
    split = None if "," not in value else ","
    tags = [tag.strip() for tag in value.split(split)]
    tags_html = ['<a href="%s">%s</a>' % \
        (reverse('web:posts', kwargs={'tag':tagname}), tagname) for tagname in tags]
    return mark_safe(", ".join(tags_html))
