# -*- coding: utf-8 -*-

from niwi.admin import GenericModelAdmin
from niwi_apps.filepaste.models import WebFile

from django.contrib import admin
import datetime

class WebFileModelAdmin(GenericModelAdmin):
    save_on_top = True
    list_display = ('id', 'description', 'created_date', 'hidden')
    list_display_links = list_display
    prepopulated_fields = {"slug": ("description",)}


admin.site.register(WebFile, WebFileModelAdmin)
