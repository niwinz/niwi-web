# -*- coding: utf-8 -*-

from niwi.web.models import *
from django.contrib import admin
import datetime

class GenericModelAdmin(admin.ModelAdmin):
    class Media:
        css = {'all':('css/admin.css',)}

    def save_model(self, request, obj, form, change):
        if change and hasattr(obj, 'modified_date'):
            obj.modified_date = datetime.datetime.now()

        super(GenericModelAdmin, self).save_model(request, obj, form, change)


class PostAttachmentInline(admin.TabularInline):
    model = PostAttachment
    extra = 1
    can_delete = True
    prepopulated_fields = {"slug": ("name",)}


class PostModelAdmin(GenericModelAdmin):
    save_on_top = True
    search_fields = ('title', 'slug', 'uuid')
    list_display = ('id', 'title', 'created_date', 'modified_date', 'status', 'owner')
    list_display_links = list_display
    list_filter = ('status', 'created_date')
    fieldsets = (
        ('Head', {
            'fields': ('title', 'slug', 'tags', ('markup', 'status'),)
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('created_date', 'modified_date', 'owner'),
        }),
    )
    inlines = [PostAttachmentInline]
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(PostModelAdmin, self).save_model(request, obj, form, change)


class PageModelAdmin(PostModelAdmin):
    fieldsets = (
        ('Head', {
            'fields': ('title', 'slug', ('markup', 'status'),)
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('created_date', 'modified_date', 'owner'),
        }),
    )

    inlines = []


class BookmarkModelAdmin(GenericModelAdmin):
    search_fields = ('title',)
    list_display = ('id','title', 'public', 'owner')
    list_display_links = list_display
    list_filter = ('created_date', 'modified_date', 'public',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(BookmarkModelAdmin, self).save_model(request, obj, form, change)


class PasteModelAdmin(GenericModelAdmin):
    search_fields = ('text','title')
    list_display = ('id', 'title', 'lexer', 'created')
    list_display_links = list_display
    list_filter = ('lexer', 'created')




admin.site.register(Post, PostModelAdmin)
admin.site.register(Bookmark, BookmarkModelAdmin)
admin.site.register(Paste, PasteModelAdmin)
admin.site.register(Page, PageModelAdmin)
