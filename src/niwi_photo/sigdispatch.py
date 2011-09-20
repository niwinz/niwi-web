# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

from niwi_photo.models import Photo
from niwi_photo.image import ImageAdapter

import tempfile

@receiver(post_save, sender=Photo)
def photo_post_save(sender, instance, created, **kwargs):
    """ Create resized images for photo instance. """
    
    if created:
        if not instance.large:
            f1 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
            instance.large = ImageAdapter.resize(instance.original.path, f1, 1200)

        if not instance.medium:
            f2 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
            instance.medium = ImageAdapter.resize(instance.original.path, f2, 900)
        
        if not instance.small:
            f3 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True)
            instance.small = ImageAdapter.resize(instance.original.path, f3, 450)

        if not instance.square:
            f4 = tempfile.NamedTemporaryFile(suffix=".jpg", delete=True) 
            instance.square = ImageAdapter.square(instance.original.path, f4)

        instance.save()
