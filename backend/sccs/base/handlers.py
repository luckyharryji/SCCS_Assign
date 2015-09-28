#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, json_decode
from .models import db

class BaseHandler(RequestHandler):
    def success_response(self,content=None):
        if isinstance(content,str):
            try:
                content=json_decode(content)
            except :
                pass
        result = {'status':200,'errorMessage':None,'data':content}
        self.write(json_encode(result))

    def fail_response(self, status_code, error_message):
        '''
        return the message info when connection error
        '''
        result = {'status':status_code, 'error_message':error_message, 'data':None}
        self.set_status(status_code)
        self.write(json_encode(result))

    def get_current_user(self):
        return self.get_secure_cookie("user")
