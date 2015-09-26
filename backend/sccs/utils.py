#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import url
from .settings import PROJECT_NAME

def union_urls(urls):
    _urls = list(urls)
    urls = []
    for prefix, module_name in _urls:
        obj = __import__('%s.%s' % (PROJECT_NAME,module_name),fromlist=[PROJECT_NAME])
        sub_urls = getattr(obj,'urls')
        for u,h in sub_urls:
            urls.append(url('%s%s' % (prefix,u),h))
            print prefix
            print u
            print h
    return urls

def get_int_value(value, default=None):
    '''
    transfer the type of the input
    '''
    try:
        return int(value)
    except:
        return default
