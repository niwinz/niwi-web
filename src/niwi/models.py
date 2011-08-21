# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from niwi.utils import get_url_data
from niwi.forms.paste import LEXER_CHOICES
from niwi.contrib.db.fields import CreationDateTimeField, ModificationDateTimeField

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


class Page(models.Model):
    slug  = models.SlugField(unique=True, db_index=True, editable=True)
    title = models.CharField(max_length=500, db_index=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')

    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

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
    title = models.CharField(max_length=500, db_index=True, blank=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')

    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)
    
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
    slug = models.SlugField(unique=True, db_index=True, editable=True, blank=True)
    url = models.CharField(max_length=1000, unique=True, db_index=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'links'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title, body = get_url_data(self.url)

        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)

        super(Link, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-link', (), {'slug': self.slug})


class Config(models.Model):
    google_analytics_domain = models.CharField(max_length=200, blank=True)
    google_analytics_code = models.CharField(max_length=200, blank=True)
    core_homepage = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'config'


class Paste(models.Model):
    text = models.TextField()
    lexer = models.CharField(max_length=5)
    title = models.CharField(max_length=100, blank=True)
    group = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'paste'
