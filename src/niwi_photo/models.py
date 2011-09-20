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
import datetime, uuid

class Album(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    def __unicode__(self):
        return u"Album: %s" % (self.name)

class Photo(models.Model):
    album = models.ForeignKey('niwi_photo.Album', related_name='photos')
    small_description = models.CharField(max_length=300)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    exifdata = DictField()

    original = models.ImageField(max_length=200, upload_to='original/%Y/%m/%d')
    large = models.ImageField(max_length=200, upload_to='large/%Y/%m/%d',
        serialize=False, editable=False) # Max 1200px
    medium = models.ImageField(max_length=200, upload_to='medium/%Y/%m/%d',
        serialize=False, editable=False) # Max 900px
    small = models.ImageField(max_length=200, upload_to='small/%Y/%m/%d',
        serialize=False, editable=False) #max 450px
    square = models.ImageField(max_length=200, upload_to='square/%Y/%m/%d', 
        serialize=False, editable=False, null=True) # 120x120

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.small_description, self.__class__)

        super(Photo, self).save(*args, **kwargs)
