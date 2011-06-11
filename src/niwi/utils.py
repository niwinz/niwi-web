# -*- coding: utf-8 -*-

from lxml.html import parse, tostring

class Singleton(type):
    """ Singleton metaclass. """

    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance


def get_url_data(url):
    element = parse(url)
    title_obj = element.getroot().cssselect('title')[0]
    return (title_obj.text_content(), tostring(title_obj.body))
