# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django import forms

from niwi.paste.models import RestrictedLog
import datetime

LEXER_CHOICES = (
    ('', '---------'),
    ('text', 'Text plain'),
    ('c', 'C'),
    ('cpp', 'C++'),
    ('d', 'D'),
    ('csharp', 'C#'),  
    ('go', 'Go'),
    ('java', 'Java'),
    ('py', 'Python 2.x'),
    ('py3', 'Python 3.x'),
    ('php', 'PHP'),
    ('pl', 'Perl'),
    ('rb', 'Ruby'),
    ('vala', 'Vala'),
    ('css', 'CSS'),
    ('html', 'HTML/XHTML'),
    ('js', 'JavaScript'),
    ('xml', 'XML'),
    ('html+php', 'HTML+PHP'),
    ('html+django', 'HTML+Django'),
)

class PasteForm(forms.Form):
    paste = forms.CharField(widget=forms.Textarea, label=_(u"Paste content"))
    lexer = forms.ChoiceField(choices=LEXER_CHOICES, label=_(u"Lexer"))
    title = forms.CharField(max_length=100, required=False, label=_(u"Title"))
    group = forms.CharField(max_length=50, required=False, label=_(u"Group"))

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request')
        super(PasteForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        
        real_ip = "HTTP_X_REAL_IP" in self._request.META and self._request.META['HTTP_X_REAL_IP'] \
           or self._request.META['REMOTE_HOST']
       
        try:
            robj = RestrictedLog.objects.get(host=real_ip)
            stamp_control = datetime.datetime.now() - datetime.timedelta(seconds=15)
            if robj.stamp > (datetime.datetime.now() - datetime.timedelta(seconds=15)):
                self._errors['paste'] = self.error_class([u'No puede publicar mas de un paste en 15 segundos.'])
            else:
                robj.stamp = datetime.datetime.now()
                robj.save()

        except RestrictedLog.DoesNotExist:
            RestrictedLog.objects.create(host=real_ip, stamp=datetime.datetime.now())

        return cleaned_data
