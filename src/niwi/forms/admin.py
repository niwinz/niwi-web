# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from ..models.admin import User

class LoginForm(forms.Form):
    username = forms.EmailField(required=True, label=_(u'Your email'))
    password = forms.CharField(required=True, label=_(u'Your password'),
        wisget=forms.PasswordInput)

    def clean(self):
        cleaned_data = self.cleaned_data
        if "username" in cleaned_data:
            userobj = User.objects(username=cleaned_data['username']).first()
            if not userobj:
                self._errors['username'] = self.error_class([_(u'Username not exists.')])
                del cleaned_data['username']
                del cleaned_data['password']

            else:
                if not userobj.check_password(cleaned_data.get('password', '!')):
                    self._errors['username'] = self.error_class([_(u'Incorrect password.')])
                else:
                    self._user = userobj
        return cleaned_data

    def authenticate(self, request):
        request.session['user_username'] = self._user.username
        request.session['user_id'] = self._user.id
        return True
        
        


