# -*- coding: utf-8 -*-

from django.contrib.auth.utils import make_password, check_password
from django.db import models

from niwi.models import slugify_uniquely
import datetime

class WebFile(models.Model):
    desciption = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    attached_file = models.FileField(max_length=1000, upload_to="filepaste/%Y/%m/%d",
        serialize=False, editable=True, blank=False)
    created_date = models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)
    password = models.CharField(max_length=200, blank=True, null=True, default='')
    hidden = models.BooleanField(default=False)

    def set_password(self, raw_password):
        self.password = make_password('sha1', raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.desciption, self.__class__)

        super(WebFile, self).save(*args, **kwargs)
