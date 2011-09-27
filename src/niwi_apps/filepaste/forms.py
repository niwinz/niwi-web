# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from niwi_apps.filepaste.models import WebFile


class UploadForm(ModelForm):
    class Meta:
        model = WebFile
        fields = ('description', 'attached_file', \
                    'password', 'hidden')
