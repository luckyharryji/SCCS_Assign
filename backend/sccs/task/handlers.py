#!/usr/bin/env python
# -*-coding:utf-8-*-
from tornado.web import HTTPError,MissingArgumentError
import json
from ..base.handlers import BaseHandler

class TaskListHandler(BaseHandler):
    def get(self):
        return self.success_response(json.dumps({"name":"test"}))

    def post(self):
        return self.success_response(json.dumps({"name":"test"}))
