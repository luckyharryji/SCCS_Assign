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
        if status not in (2, 3, 4, 5):
            status = 2
        tasks = task_api.get_task_list(status, type, order, desc, page_num, page_amount)
        return self.success_response([t.to_json(simple=True) for t in tasks])

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


class TaskDetailHandler(BaseHandler):
    def get(self, task_id):
        '''
        get task
        '''
        try:
            t = task_api.get_task_by_id(task_id)
            return self.success_response(t.to_json())
        except DoesNotExist:
            return self.fail_response(400, u'task does not exist')

    def post(self, task_id):
        '''
        claim to do the task
        '''
        try:
            name = escape.xhtml_escape(self.current_user)
            login_user = user_api.get_user_by_name(name)
            t = task_api.get_task_by_id(task_id)
            if t.status != 2:
                raise HTTPError(status_code=400, reason=u'status wrong')
            founder = mid_credit_api.get_task_founder(t)
            if login_user.id in [f['user'].id for f in founder]:
                raise HTTPError(status_code=400, reason=u'can not be done by provider')
            t.pick_date = datetime.now()
            t.save()
            task_api.add_task_worker(t, login_user)
            if len(task_api.get_task_worker(t)) >= t.max_worker:
                t = task_api.update_task_status(t, 3)
            return self.success_response(t.to_json())
        except HTTPError as e:
            return self.fail_response(e.status_code, e.reason)
        except DoesNotExist:
            return self.fail_response(400, u'task does not exist')


    def put(self, task_id):
        '''
        edit task: except cresit and status
        '''
        try:
            name = escape.xhtml_escape(self.current_user)
            login_user = user_api.get_user_by_name(name)
            t = task_api.get_task_by_id(task_id)
            if t.status in (4, 5, 6):
                raise HTTPError(status_code=400, reason=u'task status missing')
            if login_user.id != t.creator.id:
                raise HTTPError(status_code=400, reason=u'no authorization')
            title = self.get_argument('title')
            content = self.get_argument('content')
            end_date = datetime.strptime(self.get_argument('end_date'), '%Y-%m-%d')
            addition = self.get_argument('addition', None)
            t = task_api.update_task_content(t, title, content, end_date, addition)
            return self.success_response(t.to_json())
        except HTTPError as e:
            return self.fail_response(e.status_code, e.reason)


    def delete(self, task_id):
        '''
        close the task
        '''
        try:
            name = escape.xhtml_escape(self.current_user)
            login_user = user_api.get_user_by_name(name)
            t = task_api.get_task_by_id(task_id)
            if login_user.id != t.creator.id:
                raise HTTPError(status_code=400, reason=u'no authority')
            if t.status > 3:
                raise HTTPError(status_code=400, reason=u'task status missing')
            t = task_api.update_task_status(t, 6)
            return self.success_response(t.to_json())
        except HTTPError as e:
            return self.fail_response(e.status_code, e.reason)
        except DoesNotExist:
            return self.fail_response(400, u'task does not exist')


class FounderHandler(BaseHandler):
    def post(self, task_id, credit):
        '''
        founder who can add credit for the task
        '''
        try:
            name = escape.xhtml_escape(self.current_user)
            login_user = user_api.get_user_by_name(name)
            t = task_api.get_task_by_id(task_id)
            if t.status != 2:
                raise HTTPError(status_code=400, reason=u'task status missing')
            task_api.add_task_founder(login_user, t, int(credit))
            return self.success_response(t.to_json())
        except HTTPError as e:
            return self.fail_response(e.status_code, e.reason)
        except DoesNotExist:
            return self.fail_response(400, u'task does not exist')
