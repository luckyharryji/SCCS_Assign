#!/usr/bin/env python
# -*-coding:utf-8-*-
from tornado.web import HTTPError,MissingArgumentError
from tornado import escape

import json
from ..base.handlers import BaseHandler
from ..utils import get_int_value
from ..user import api as user_api
from . import api as task_api

from datetime import datetime

class TaskListHandler(BaseHandler):
    def get(self):
        '''
        get the list of the tasks that tend to be solved
        '''
        page_num = get_int_value(self.get_argument('page',1),1)
        page_amount = get_int_value(self.get_argument('num',20),20)
        status = get_int_value(self.get_argument('status',2),2)
        type = get_int_value(self.get_argument('type',None))
        order = self.get_argument('order','time')
        desc = get_int_value(self.get_argument('desc',1),1)
        print "page_num ",page_num

        return self.success_response(json.dumps({"name":"test"}))

    def post(self):
        '''
        create a new task in the system
        '''
        try:
            name = escape.xhtml_escape(self.current_user)
            print name
            creator = user_api.get_user_by_name(name)
            try:
                type = int(self.get_argument('type',0))
            except ValueError:
                type = 0
            title = self.get_argument('title')
            content = self.get_argument('content')
            end_date = datetime.strptime(self.get_argument('end_date'),'%Y-%m-%d')
            addition = self.get_argument('addition',None)
            try:
                credit = int(self.get_argument('credit'))
                setting_name = type == 0 and 'easy_task_base_credit' or 'hard_task_base_credit'
            except ValueError:
                return self.fail_response(400,'wrong parameter')
        except MissingArgumentError:
            return self.fail_response(400,'missing argument')
        except HTTPError as e:
            return self.fail_response(e.status_code,'HTTP Error: %s' % e.reason)
        try:
            if type == 2:
                try:
                    max_worker = int(self.get_argument('max_worker', 1))
                except ValueError:
                    max_worker = 1
                t = task_api.create_task(type, title, content, end_date, addition, credit, creator, max_worker)
            else:
                t = task_api.create_task(type, title, content, end_date, addition, credit, creator, 1)
        except AssertionError:
            return self.fail_response(400, u'Credit is not enough')
        return self.success_response(t.to_json())
