# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.conf import settings
import base64

try:
    from Crypto.Cipher import Blowfish
except ImportError:
    raise ImportError('Using an encrypted field requires the pycripto. You can install pycripto with "pip install pycrypto"')


class BaseEncryptedField(models.Field):
    __prefix = 'string_enc::'
    
    def __init__(self, *args, **kwargs):
        self.cipher = Blowfish.new(settings.SECRET_KEY[:10])
        super(BaseEncryptedField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value.startswith(self.__prefix):
            decrypted_value = self.cipher.decrypt(base64.b64decode(value[len(self.__prefix):]))
            rest = decrypted_value.index('\0')
            if rest > 0:
                decrypted_value = decrypted_value[:rest]
            return decrypted_value.decode('utf-8')
        else:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value.startswith(self.__prefix):
            value = value.encode('utf-8')
            if len(value) % 8 != 0:
                counter = 8 - (len(value) % 8)
                value = value + "\0" * counter
            return self.__prefix + base64.b64encode(self.cipher.encrypt(value))
        return value


class EncryptedTextField(BaseEncryptedField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, **kwargs):
        defaults = {'widget': forms.Textarea}
        defaults.update(kwargs)
        return super(EncryptedTextField, self).formfield(**defaults)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

