# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from niwi.utils import get_url_data, cacheable
from niwi.forms import LEXER_CHOICES
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
    slug  = models.SlugField(max_length=100, unique=True, db_index=True, editable=True, blank=True)
    title = models.CharField(max_length=500, db_index=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')
    owner = models.ForeignKey('auth.User', related_name='pages', null=True, default=None, blank=True)
    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)

    # Only for test new features on django_postgresql
    aditional_indexes = [
        ('%(tablename)s_title_gist_idx0', 'btree', 'lower(title)', 'varchar_pattern_ops'),
    ]

    class Meta:
        db_table = 'pages'

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-page', (), {'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)

        super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Page: %s" % (self.title)


class Post(models.Model):
    slug  = models.SlugField(max_length=100, unique=True, db_index=True, editable=True, blank=True)
    title = models.CharField(max_length=500, db_index=True, blank=True)
    content = models.TextField()
    markup = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='posts', null=True, default=None, blank=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, db_index=True, default='draft')
    tags = models.CharField(max_length=200, blank=True, null=True, default='', db_index=True)

    created_date = CreationDateTimeField(editable=True)
    modified_date = ModificationDateTimeField(editable=True)
    
    class Meta:
        db_table = 'posts'

    def __unicode__(self):
        return u"Post: %s" % (self.title) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)

        super(Post, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-post', (), {'slug': self.slug})


class Bookmark(models.Model):
    title = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, editable=True, blank=True)
    url = models.CharField(max_length=1000, unique=True, db_index=True)
    tags = models.CharField(max_length=1000, db_index=True, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='bookmarks', blank=True, null=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return u"Bookmark: %s" % (self.title)

    class Meta:
        db_table = 'bookmarks'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title, body = get_url_data(self.url)
        if not self.slug:
            self.slug = slugify_uniquely(self.title, self.__class__)
        super(Bookmark, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('web:show-bookmark', (), {'slug': self.slug})


class ConfigManager(models.Manager):
    """ 
    TODO: improve cacheable decorator to generate key 
    automaticaly for method name and this docstring.
    """

    @property
    @cacheable("google_analytics_domain", timeout=30)
    def google_analytics_domain(self):
        queryset = self.get_query_set().filter(key="google.analytics.domain")
        return queryset.get().val if len(queryset) else ""

    @property
    @cacheable("google_analytics_code", timeout=30)
    def google_analytics_code(self):
        queryset = self.get_query_set().filter(key="google.analytics.code")
        return queryset.get().val if len(queryset) else ""

    @property
    @cacheable("home_page", timeout=20)
    def home_page(self):
        queryset = self.get_query_set().filter(key="core.homepage")
        return queryset.get().val if len(queryset) else None

    @property
    @cacheable("show_photo_on_homepage", timeout=30)
    def show_photo_on_homepage(self):
        queryset = self.get_query_set().filter(key="core.photo_on_homepage")
        return True if len(queryset) and queryset.get().val == "1" else False

    @property
    @cacheable("show_entries_on_homepage", timeout=30)
    def show_entries_on_homepage(self):
        queryset = self.get_query_set().filter(key="core.entries_on_homepage")
        return True if len(queryset) and queryset.get().val == "1" else False

    @property
    @cacheable("host", timeout=60)
    def host(self):
        queryset = self.get_query_set().filter(key="core.host")
        return queryset.get().val if len(queryset) else ''
    
    @property
    @cacheable("disqus_shortname", timeout=60)
    def disqus_shortname(self):
        queryset = self.get_query_set().filter(key="disqus.shortname")
        return queryset.get().val if len(queryset) else ''

    @property
    @cacheable("twitter_referer", timeout=60)
    def twitter_referer(self):
        queryset = self.get_query_set().filter(key="twitter.referrer")
        return queryset.get().val if len(queryset) else ''



class Paste(models.Model):
    text = models.TextField()
    lexer = models.CharField(max_length=5)
    title = models.CharField(max_length=100, blank=True)
    group = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"Paste: %s" % (self.title)

    class Meta:
        db_table = 'paste'
