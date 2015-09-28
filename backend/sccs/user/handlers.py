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

class ShowPeopleCreditHandler(BaseHandler):
    def get(self,userid):
        '''
        credit change in rank list
        '''
        target_user = user_api.get_user_by_id(userid)
        all_log = get_int_value(self.get_argument('all',None),None)
        if all_log == 1:
            logs = mid_credit_api.get_credit_log_by_user(target_user,num='all')
        else:
            logs = mid_credit_api.get_credit_log_by_user(target_user)
        mids = mid_credit_api.get_mid_credit_from_user(target_user)
        result = {'log':[log.to_json() for log in logs],'middle':[m.to_json() for m in mids if m.credit > 0]}
        return self.success_response(result)
