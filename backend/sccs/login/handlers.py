#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode,json_decode
from peewee import DoesNotExist
# need to add exception to catch duplicate error

from ..base.handlers import BaseHandler
from ..base.models import db

from ..user import api as user_api


class RegisHandler(BaseHandler):
    def post(self):
        '''
        regis a new user
        '''
        email = self.get_argument('email')
        name = self.get_argument('name')
        password = self.get_argument('password')
        print email
        print name
        print password
        try:
            result = user_api.get_user_by_name(name).to_json()
            self.success_response(result)
        except DoesNotExist:
            result=user_api.create_user(email,name,password).to_json()
            self.success_response(result)

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
