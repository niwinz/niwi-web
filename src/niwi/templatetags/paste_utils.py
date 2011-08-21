# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name="default_title")
def default_title(title):
    return title or "Sin titulo"
