#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, json_decode

class BaseHandler(RequestHandler):
    def success_response(self,content=None):
        if isinstance(content,str):
            try:
                content=json_decode(content)
            except :
                pass
        result = {'status':200,'errorMessage':None,'data':content}
        self.write(json_encode(result))
