# -*- coding: utf-8 -*-

import Image
from django.core.files import File

class ImageAdapter(object):
    @staticmethod
    def square(imgpath, savefile, size=300, quality=98):
        """
        Method for generate 100x100 square thumbnails.
        """
        sqsize = (size, size)
        img = Image.open(imgpath)
        width, height = img.size

        if width > height:
           delta = width - height
           left = int(delta/2)
           upper = 0
           right = height + left
           lower = height
        else:
           delta = height - width
           left = 0
           upper = int(delta/2)
           right = width
           lower = width + upper

        img = img.crop((left, upper, right, lower))
        img.thumbnail(sqsize, Image.ANTIALIAS)
        img.save(savefile, quality=quality)

        return File(savefile)

    @staticmethod
    def resize(imgpath, savefile, maxsize, quality=100):
        img = Image.open(imgpath)
        img.thumbnail((maxsize, maxsize), Image.ANTIALIAS)
        img.save(savefile, quality=quality)
        return File(savefile)
