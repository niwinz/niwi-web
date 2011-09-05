# -*- coding: utf-8 -*-
from niwi.models import *

from django.contrib import admin
import datetime


def make_published(modeladmin, request, queryset):
    queryset.update(status='public')


def make_private(modeladmin, request, queryset):
    queryset.update(status='private')


class GenericModelAdmin(admin.ModelAdmin):
    class Media:
        css = {'all':('css/admin.css',)}

    def save_model(self, request, obj, form, change):
        if change and hasattr(obj, 'modified_date'):
            obj.modified_date = datetime.datetime.now()

        super(GenericModelAdmin, self).save_model(request, obj, form, change)


class GenericPostModelAdmin(GenericModelAdmin):
    save_on_top = True
    search_fields = ('title', 'slug', 'uuid')
    list_display = ('id', 'title', 'created_date', 'modified_date', 'status',)
    list_display_links = list_display
    list_filter = ('status', 'created_date')
    #exclude = ('content_type',)
    fieldsets = (
        ('Head', {
            'fields': ('title', 'slug', ('markup', 'status'),)
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('created_date', 'modified_date'),
        }),
    )
    actions = [make_published, make_private]


class LinkModelAdmin(GenericModelAdmin):
    search_fields = ('title',)
    list_display = ('id','title', 'public',)
    list_display_links = list_display
    list_filter = ('created_date', 'modified_date', 'public',)
    actions = [make_published, make_private]


class PasteModelAdmin(GenericModelAdmin):
    search_fields = ('text','title')
    list_display = ('id', 'title', 'lexer', 'created')
    list_display_links = list_display
    list_filter = ('lexer', 'created')


admin.site.register(Post, GenericPostModelAdmin)
admin.site.register(Link, LinkModelAdmin)
admin.site.register(Paste, PasteModelAdmin)
admin.site.register(Page, GenericPostModelAdmin)
admin.site.register(Config)
