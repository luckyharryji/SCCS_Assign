#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import DoesNotExist
from tornado.web import MissingArgumentError
from tornado import escape

from ..base.handlers import BaseHandler
from . import api as comment_api
from ..task import api as task_api
from ..user import api as user_api
from ..utils import get_int_value

class TaskCommentHandler(BaseHandler):
    def get(self):
        '''
        get comment of a task, order by time
        '''
        try:
            taskid = get_int_value(self.get_argument('taskid'))
            t = task_api.get_task_by_id(taskid)
        except DoesNotExist:
            return self.fail_response(400,u'task does not exist')
        except MissingArgumentError:
            return self.fail_response(400,u'wrong parameter')
        comments = comment_api.get_comment_by_task(t)
        return self.success_response([c.to_json(simple=True) for c in comments])


    def post(self):
        '''
        adding comment
        Data:
            taskid
            content
            reply  optional
        '''
        name = escape.xhtml_escape(self.current_user)
        login_user = user_api.get_user_by_name(name)
        try:
            taskid = self.get_argument('taskid')
            content = self.get_argument('content')
            reply = self.get_argument('reply',None)
            if reply:
                reply = user_api.get_user_by_id(reply)
            else:
                reply = None
            t = task_api.get_task_by_id(taskid)
        except MissingArgumentError:
            return self.fail_response(400,u'wrong parameter')
        except DoesNotExist:
            return self.fail_response(400,u'task does not exist')
        # add comment
        c = comment_api.add_comment(t,login_user,content,reply)
        # email
        to = list()
        return self.success_response(c.to_json())
