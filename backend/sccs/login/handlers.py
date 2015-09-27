#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode,json_decode
from peewee import DoesNotExist

from ..base.handlers import BaseHandler
from ..base.models import db

class LoginHandler(BaseHandler):
    def post(self):
        '''
        add new user register info
        '''
        email = self.get_argument('email')
        name = self.get_argument('name')
        passward = self.get_argument('passward')
        try:
            #get user info by email from user api
            return
        except DoesNotExist:
            # create a new user from user api
            return
