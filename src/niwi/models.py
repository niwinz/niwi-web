# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from niwi.utils import get_url_data
from niwi.paste.forms import LEXER_CHOICES
from niwi.contrib.db.fields import UUIDField, CreationDateTimeField, \
    ModificationDateTimeField, AutoSlugField

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

import datetime, uuid

STATUS_CHOICES = (
    ('public', u'Public'),
    ('private', u'Private'),
    ('draft', u'Draft'),
)

def slugify_uniquely(value, model, slugfield="slug"):
    suffix = 0
    potential = base = slugify(value)
    if len(potential) == 0:
        potential = 'null'
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix += 1


class Page(models.model):
    slug  = models.SlugField(unique=True, db_index=True, editable=True)
    #slug = AutoSlugField(populate_from='title', unique=True, db_index=True, editable=True)
    title = models.CharField(max_length=500, db_index=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')
    lang = models.CharField(max_length=10, choices=settings.LANGUAGES)

    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

    current_version = models.IntegerField(default=1)
    parent_version = models.IntegerField(null=True, default=None, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, default=None)
    class Meta:
        db_table = 'pages'

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-page', (), {'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)

        super(Page, self).save(*args, **kwargs)


class Post(models.Model):
    slug  = models.SlugField(unique=True, db_index=True, editable=True)
    #slug = AutoSlugField(populate_from='title', unique=True, db_index=True, editable=True)
    title = models.CharField(max_length=500, db_index=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')

    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

    current_version = models.IntegerField(default=1)
    parent_version = models.IntegerField(null=True, default=None, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, default=None)

    class Meta:
        db_table = 'posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)

        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-post', (), {'slug': self.slug})


class Link(models.Model):
    title = models.CharField(max_length=500, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    url = models.CharField(max_length=1000)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'links'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title, body = get_url_data(self.url)
        
        super(Link, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-link', (), {'slug': self.slug})


class Config(models.Model):
    path = models.CharField(max_length=200, unique=True, db_index=True)
    value = models.CharField(max_length=500, blank=True)

    created_date = CreationDateTimeField()
    modified_date = ModificationDateTimeField()

    class Meta:
        db_table = 'config'
