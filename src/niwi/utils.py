# -*- coding: utf-8 -*-

from lxml.html import parse, tostring

def get_url_data(url):
    element = parse(url)
    title_obj = element.getroot().cssselect('title')[0]
    return (title_obj.text_content(), tostring(title_obj.body))
