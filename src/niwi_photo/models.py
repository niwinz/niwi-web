# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from niwi.contrib.db.fields import CreationDateTimeField
from niwi.contrib.db.fields import ModificationDateTimeField
from niwi.contrib.db.fields import DictField

from niwi.models import slugify_uniquely
from niwi_photo.image import ImageAdapter

import datetime, uuid, tempfile, os


class Album(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    
    owner = models.ForeignKey('auth.User', related_name='albums', null=True, blank=True)
    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

    def __unicode__(self):
        return u"Album: %s" % (self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('photo:show-album', (), {'aslug':self.slug})


class Photo(models.Model):
    album = models.ForeignKey('niwi_photo.Album', related_name='photos')
    small_description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    exifdata = DictField(editable=True)

    original = models.ImageField(max_length=200, upload_to='original/%Y/%m/%d')
    large = models.ImageField(max_length=200, upload_to='large/%Y/%m/%d',
        serialize=False, editable=True, blank=True) # Max 1200px
    medium = models.ImageField(max_length=200, upload_to='medium/%Y/%m/%d',
        serialize=False, editable=True, blank=True) # Max 900px
    small = models.ImageField(max_length=200, upload_to='small/%Y/%m/%d',
        serialize=False, editable=True, blank=True) #max 450px
    square = models.ImageField(max_length=200, upload_to='square/%Y/%m/%d', 
        serialize=False, editable=True, blank=True, null=True) # 120x120

    owner = models.ForeignKey('auth.User', related_name='photos', null=True, blank=True)
    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

    def __unicode__(self):
        return u"Photo: %s" % (self.small_description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.small_description, self.__class__)
        
        super(Photo, self).save(*args, **kwargs)

    @property
    def desc_html(self):
        return u"<a href='%s'>%s" % ('', self.small_description)


    def rehash_thumbnails(self, commit=False):
        if self.large and os.path.exists(self.large.path): 
            os.remove(self.large.path)
        if self.medium and os.path.exists(self.medium.path): 
            os.remove(self.medium.path)
        if self.small and os.path.exists(self.small.path): 
            os.remove(self.small.path)
        if self.square and os.path.exists(self.square.path): 
            os.remove(self.square.path)
    
        f1 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
        self.large = ImageAdapter.resize(self.original.path, f1, 1200)
    
        f2 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
        self.medium = ImageAdapter.resize(self.original.path, f2, 900)
            
        f3 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
        self.small = ImageAdapter.resize(self.original.path, f3, 450)
    
        f4 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) 
        self.square = ImageAdapter.square(self.original.path, f4)
        self.exifdata = ImageAdapter.get_exif_dict(self.original.path)

        if commit:
            self.save()
