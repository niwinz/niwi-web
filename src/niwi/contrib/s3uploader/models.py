# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class Upload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    path = models.CharField(max_length=200)
    size = models.CharField(max_length=200)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return u"<Upload object %(id)d>" % {'id':self.id}

    def full_url(self):
        return settings.AWS_BASE_URL + self.path

    @models.permalink
    def get_absolute_url(self):
        return ('s3uploader:file', (), {'id':self.id})
