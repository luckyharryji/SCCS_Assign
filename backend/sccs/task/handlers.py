#!/usr/bin/env python
# -*-coding:utf-8-*-
from tornado.web import HTTPError,MissingArgumentError
import json
from ..base.handlers import BaseHandler
from ..utils import get_int_value

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
        return self.success_response(json.dumps({"name":"test"}))
