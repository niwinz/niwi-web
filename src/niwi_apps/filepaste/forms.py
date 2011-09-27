# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.forms import ModelForm
from niwi_apps.filepaste.models import WebFile


class UploadForm(ModelForm):
    class Meta:
        model = WebFile
        fields = ('description', 'attached_file', \
                    'password', 'hidden')

class DownloadForm(forms.Form):
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.wfile = kwargs.pop('wfile')
        super(DownloadForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        if "password" in cleaned_data:
            if not self.wfile.check_password(cleaned_data['password']):
                self._errors['password'] = self.error_class([_(u'Incorrect password')])
                del cleaned_data['password']
            
