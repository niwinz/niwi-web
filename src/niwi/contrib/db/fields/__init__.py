# -*- coding: utf-8 -*-
# Copyright (c) 2011 Andrei Antoukh <niwi@niwi.be>
# License: BSD-3 
# Version: 5

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models import DateTimeField, CharField, SlugField

from base64 import b64encode, b64decode
import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle


class CreationDateTimeField(DateTimeField):
    """ CreationDateTimeField

    By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', datetime.datetime.now)
        DateTimeField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class ModificationDateTimeField(CreationDateTimeField):
    """ ModificationDateTimeField

    By default, sets editable=False, blank=True, default=datetime.now

    Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = datetime.datetime.now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.DateTimeField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class DictField(models.Field):
    """ Dictionary pickled field. """
    __metaclass__ = models.SubfieldBase
    __prefix__ = "pickle_dict::"
    __pickleproto__ = -1

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', {})
        kwargs.setdefault('blank', True)
        super(DictField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if isinstance(value, (str, unicode)) and value.startswith(self.__prefix__):
            local_value = value[len(self.__prefix__):]
            return pickle.loads(b64decode(str(local_value)))
        else:
            return {}

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is not None:
            if isinstance(value, dict):
                value = self.__prefix__ + b64encode(pickle.dumps(value, protocol=self.__pickleproto__))
            else:
                raise TypeError('This field can only store dictionaries.')
        
        return value

    def get_internal_type(self): 
        return 'TextField'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class ListField(models.Field):
    """ Pickled list field. """
    __metaclass__ = models.SubfieldBase
    __prefix__ = "pickle_list::"
    __pickleproto__ = -1

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', [])
        kwargs.setdefault('blank', True)
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, (list,tuple)):
            return value
        
        if isinstance(value, (str, unicode)) and value.startswith(self.__prefix__):
            local_value = value[len(self.__prefix__):]
            return pickle.loads(b64decode(str(local_value)))
        else:
            return []

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is not None:
            if isinstance(value, (list,tuple)):
                value = self.__prefix__ + b64encode(pickle.dumps(value, protocol=self.__pickleproto__))
            else:
                raise TypeError('This field can only store list or tuple objects')

        return value

    def get_internal_type(self):
        return 'TextField'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class CSVField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(CSVField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class IntegerListField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(IntegerListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return map(int, value.split(self.token))

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join(map(unicode, value))

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.TextField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

