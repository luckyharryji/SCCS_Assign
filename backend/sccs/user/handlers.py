#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import DoesNotExist
from tornado.web import MissingArgumentError
from tornado import escape

from ..base.handlers import BaseHandler
from . import api as user_api
from ..task import api as task_api
from ..utils import get_int_value
from ..mid_credit import api as mid_credit_api

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


class UserProfileHandler(BaseHandler):
    def get(self,userid):
        '''
        get user prodile,rank, task num
        '''
        user = user_api.get_user_by_id(userid)
        result = {
            'profile':user.to_json(simple=False),
            'rank':user_api.get_user_rank(user),
            'submit_count': task_api.get_task_by_user(0,user,return_count=True),
            'progress_count': task_api.get_task_by_user(1,user,return_count=True),
            'finish_count': task_api.get_task_by_user(2,user,return_count=True),
            'append_count': task_api.get_task_by_user(3,user,return_count=True),
        }
        return self.success_response(result)


class UserCreditHandler(BaseHandler):
    def get(self,userid):
        '''
        credit changing history
        '''
        name = escape.xhtml_escape(self.current_user)
        print name
        login_user = user_api.get_user_by_name(name)
        if login_user.id == int(userid):
            target_user = user_api.get_user_by_id(userid)
            all_log = get_int_value(self.get_argument('all',None),None)
            if all_log == 1:
                logs = mid_credit_api.get_credit_log_by_user(target_user,num='all')
            else:
                logs = mid_credit_api.get_credit_log_by_user(target_user)
            mids = mid_credit_api.get_mid_credit_from_user(target_user)
            result = {'log':[log.to_json() for log in logs],'middle':[m.to_json() for m in mids if m.credit > 0]}
            return self.success_response(result)
        else:
            return self.fail_response(400,u'authority exception')


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
