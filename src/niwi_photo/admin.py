# -*- coding: utf-8 -*-

from niwi.models import *
from niwi.admin import GenericModelAdmin

from django.contrib import admin
import datetime

class AlbumModelAdmin(GenericModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('id', 'slug', 'name',)
    list_display_links = list_display

class PhotoModelAdmin(GenericModelAdmin):
    save_on_top = True
    list_display = ('id', 'album', 'small_description')
    list_display_links = list_display

admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Album, AlbumModelAdmin)
