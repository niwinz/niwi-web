# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.template import loader

from niwi.utils import Singleton

register = template.Library()

@register.filter(name="firts_photo")
def firts_photo(album):
    photo = album.photos.all()[:1].get()
    return loader.render_to_string('photo/album_thumbnail.html',
        {'photo':photo})
