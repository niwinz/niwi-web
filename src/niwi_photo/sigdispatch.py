# -*- coding: utf-8 -*-

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.conf import settings

from niwi_photo.models import Photo
import os

@receiver(post_save, sender=Photo)
def photo_post_save(sender, instance, created, **kwargs):
    """ Create resized images for photo instance. """
    if created:
        instance.rehash_thumbnails(commit=True)


@receiver(pre_delete, sender=Photo)
def photo_pre_delete(sender, instance, **kwargs):
    if instance.large and os.path.exists(instance.large.path): 
        os.remove(instance.large.path)
    if instance.medium and os.path.exists(instance.medium.path): 
        os.remove(instance.medium.path)
    if instance.small and os.path.exists(instance.small.path): 
        os.remove(instance.small.path)
    if instance.square and os.path.exists(instance.square.path): 
        os.remove(instance.square.path)
