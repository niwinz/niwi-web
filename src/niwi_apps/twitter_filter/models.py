# -*- coding: utf-8 -*-

from django.db import models

class TwitterFilterConfig(models.Model):
    screen_name = models.CharField(max_length=200, unique=True, db_index=True)
    search_hashtag = models.CharField(max_length=200, blank=False)
    count = models.IntegerField(default=6)
    active = models.BooleanField(default=True)
