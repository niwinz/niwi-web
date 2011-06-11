# -*- coding: utf-8 -*-
from niwi.models import *
from niwi.paste.models import *

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


class GenericDocumentModelAdmin(GenericModelAdmin):
    save_on_top = True
    search_fields = ('title', 'slug', 'uuid')
    list_display = ('id', 'title', 'created_date', 'modified_date', 'status',)
    list_display_links = list_display
    list_filter = ('status', 'created_date')
    #exclude = ('content_type',)
    fieldsets = (
        ('Head', {
            'fields': ('title', 'uuid', 'slug', ('markup', 'status', 'lang'),)
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': (('current_version', 'parent_version'),'created_date', 'modified_date'),
        }),
    )
    actions = [make_published, make_private]


class WebFileInline(admin.TabularInline):
    model = WebFile
    exclude = ('uuid', )
    extra = 1

class PostModelAdmin(GenericDocumentModelAdmin):
    inlines = [WebFileInline]


class ProjectModelAdmin(GenericDocumentModelAdmin):
    pass

class DocumentModelAdmin(GenericDocumentModelAdmin):
    def queryset(self, request):
        return super(DocumentModelAdmin, self).queryset(request).filter(content_type__name='document')

class PageModelAdmin(GenericDocumentModelAdmin):
    pass



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


class ConfigModelAdmin(GenericModelAdmin):
    search_fields = ('path', 'value')
    list_display = ('path', 'value')
    list_display_links = list_display
    list_filter = ('created_date', 'modified_date')

    fieldsets = (
        (None, {
            'fields':( ('path', 'value'), )
        }),
    )


admin.site.register(Post, PostModelAdmin)
admin.site.register(Link, LinkModelAdmin)
admin.site.register(Paste, PasteModelAdmin)
admin.site.register(Project, ProjectModelAdmin)
admin.site.register(Page, PageModelAdmin)
admin.site.register(Document, DocumentModelAdmin)
admin.site.register(Config, ConfigModelAdmin)
