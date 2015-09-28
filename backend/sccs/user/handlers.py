#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import DoesNotExist
from tornado.web import MissingArgumentError
from tornado import escape

from ..base.handlers import BaseHandler
from . import api as user_api
from ..task import api as task_api
from ..utils import get_int_value

class CurrentUserHandler(BaseHandler):
    def get(self):
        '''
        get current user profile
        '''
        name = escape.xhtml_escape(self.current_user)
        print name
        user=user_api.get_user_by_name(name)
        result = user.to_json()
        return self.success_response(result)
