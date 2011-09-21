# -*- coding: utf-8 -*-

import Image, ExifTags
from django.core.files import File


exposure_translate = {
    0: 'Unidentified',
    1: 'Manual',
    2: 'Program Normal',
    3: 'Aperture Priority',
    4: 'Shutter Priority',
    5: 'Program Creative',
    6: 'Program Action',
    7: 'Portrait Mode',
    8: 'Landscape Mode'
}

color_space_translate = {
    1: 'sRGB',
    2: 'Adobe RGB',
    65535: 'Uncalibrated'
}

flash_translate = {
    0: 'No',
    1: 'Fired',
    5: 'Fired (?)', # no return sensed
    7: 'Fired (!)', # return sensed
    9: 'Fill Fired',
    13: 'Fill Fired (?)',
    15: 'Fill Fired (!)',
    16: 'Off',
    24: 'Auto Off',
    25: 'Auto Fired',
    29: 'Auto Fired (?)',
    31: 'Auto Fired (!)',
    32: 'Not Available'
}

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

    @staticmethod
    def get_raw_exif(imgpath):
        ret = {}
        img = Image.open(imgpath)
        info = img._getexif()
    
        for tag, value in info.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            ret[decoded] = value
        return ret

    @staticmethod
    def get_exif_dict(imgpath):
        rd = ImageAdapter.get_raw_exif(imgpath)
        clean_data = {}
        if "ApertureValue" in rd and isinstance(rd['ApertureValue'], tuple):
            clean_data['aperture'] = u"F%.1f" % (rd['ApertureValue'][0]/float(rd['ApertureValue'][1]))
        if 'Artist' in rd:
            clean_data['artist'] = unicode(rd['Artist'])
        if 'Copyright' in rd:
            clean_data['copyright'] = unicode(rd['Copyright'])
        if 'ExposureTime' in rd and isinstance(rd['ExposureTime'], tuple):
            clean_data['exposure'] = u"%s/%s" % (rd['ExposureTime'][0], rd['ExposureTime'][1])
        if 'FocalLength' in rd and isinstance(rd['FocalLength'], tuple):
            clean_data['focal'] = unicode(rd['FocalLength'][0]) + u"mm"
        if 'ISOSpeedRatings' in rd:
            clean_data['iso_value'] = unicode(rd['ISOSpeedRatings'])
        if 'Model' in rd:
            clean_data['camara_model'] = unicode(rd['Model'])
        if 'Software' in rd:
            clean_data['software'] = unicode(rd['Software'])
        if 'ExposureProgram' in rd:
            ep = rd['ExposureProgram']
            if ep in exposure_translate:
                clean_data['exposure_programm'] = exposure_translate[ep]
        if 'ColorSpace' in rd:
            cs = rd['ColorSpace']
            if cs  in color_space_translate:
                clean_data['color_space'] = color_space_translate[cs]

        if 'Flash' in rd:
            fl = rd['Flash']
            if fl in flash_translate:
                clean_data['flash'] = flash_translate[fl]

        return clean_data
