# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from niwi.utils import get_url_data
from niwi.paste.forms import LEXER_CHOICES
from niwi.contrib.db.fields import UUIDField, CreationDateTimeField, \
    ModificationDateTimeField, AutoSlugField

import datetime, uuid

STATUS_CHOICES = (
    ('public', u'Public'),
    ('private', u'Private'),
    ('draft', u'Draft'),
    ('deleted', u'Deleted'),
    ('versioned', u'Versioned'),
)

class Document(models.Model):
    uuid = UUIDField(unique=True, db_index=True, editable=True)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, editable=True)
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
        db_table = 'document'

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)

        super(Document, self).save(*args, **kwargs)

    def as_leaf_class(self):
        model = self.content_type.model_class()

        if model == self.__class__:
            return self
        else:
            return model.objects.get(pk=self.id)

    def __unicode__(self):
        return self.title


class WebFile(models.Model):
    uuid = UUIDField(unique=True, db_index=True, editable=True)
    document = models.ForeignKey('Document', related_name='files')
    file = models.FileField(upload_to='wf/%Y/%m/%d')

    def __unicode__(self):
        return self.uuid

    class Meta:
        db_table = 'webfile'


class Page(Document):
    class Meta:
        db_table = 'document_page'

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-page', (), {'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)


class Post(Document):
    class Meta:
        db_table = 'document_post'

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-post', (), {'slug': self.slug})


class Project(Document):
    @models.permalink
    def get_absolute_url(self):
        return ('web:show-project', (), {'slug': self.slug})

    class Meta:
        db_table = 'project'


class Link(models.Model):
    title = models.CharField(max_length=500, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    url = models.CharField(max_length=1000)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    public = models.BooleanField(default=True)

    class Meta:
        db_table = 'link'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title, body = get_url_data(self.url)
        
        super(Link, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-link', (), {'slug': self.slug})


class LinkCache(models.Model):
    link = models.ForeignKey('Link', related_name='cache')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        db_table = 'link_cache'

    def __unicode__(self):
        return u"%s/%s" % (self.link.slug, unicode(self.date))


class Config(models.Model):
    path = models.CharField(max_length=200, unique=True, db_index=True)
    value = models.CharField(max_length=500, blank=True)

    created_date = CreationDateTimeField()
    modified_date = ModificationDateTimeField()

    class Meta:
        db_table = 'config'
