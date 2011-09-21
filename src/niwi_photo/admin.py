# -*- coding: utf-8 -*-

from niwi_photo.models import *
from niwi.admin import GenericModelAdmin

from django.contrib import admin
import datetime


class PhotoModelAdmin(GenericModelAdmin):
    save_on_top = True
    list_display = ('id', 'album', 'small_description')
    list_display_links = list_display
    prepopulated_fields = {"slug": ("small_description",)}
    fieldsets = (
        ('Photo', {
            'fields': (('original', 'show_on_home'),)
        }),
        ('Photo data', {
            'fields': (('small_description', 'slug'), 'album'),
        }),
        ('Other photos', {
            'classes': ('collapse',),
            'fields': ('large', 'medium', 'small', 'square',),
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('created_date', 'modified_date', 'owner', 'exifdata'),
        })
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(PhotoModelAdmin, self).save_model(request, obj, form, change)


class PhotoInlineAdmin(admin.StackedInline):
    model = Photo
    extra = 1
    can_delete = True
    fields = (('small_description','slug'), ('original', 'show_on_home'),)
    prepopulated_fields = {"slug": ("small_description",)}


class AlbumModelAdmin(GenericModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('id', 'slug', 'name',)
    list_display_links = list_display
    prepopulated_fields = {"slug": ('name', )}
    inlines = [PhotoInlineAdmin]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug',)
        }),
        ('Metadata', {
            'fields': ('created_date','modified_date', 'owner'),
            'classes': ('collapse', ),
        })
    )
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(AlbumModelAdmin, self).save_model(request, obj, form, change)





admin.site.register(Photo, PhotoModelAdmin)
admin.site.register(Album, AlbumModelAdmin)
