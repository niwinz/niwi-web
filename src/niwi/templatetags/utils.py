# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter(name="tags_parser")
def tags_parser(tags):
    response = []
    if tags.strip():
        for tag in [x.strip() for x in tags.split(",")]:
            tagobj = u"<a href='' class='tag'>%s</a>" % (tag)
            response.append(tagobj)

    if response: return mark_safe(" ".join(response))
    else: return ""


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


   
