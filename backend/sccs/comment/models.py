#!/usr/bin/env python
# -*-coding:utf-8-*-

from peewee import TextField, ForeignKeyField

from ..base.models import BaseModel
from ..task.models import Task
from ..user.models import User

class Comment(BaseModel):
    task = ForeignKeyField(Task,related_name='comments of task')
    user = ForeignKeyField(User,related_name='user of the comment')
    content = TextField()
    reply = ForeignKeyField(User,related_name='reply to some comments',null=True)

    def to_json(self,simple=False):
        return {
            'id': self.id,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': self.user.to_json(simple=True),
            'reply': self.reply or None,
            'task_id': self.task.id,
            'content': self.content,
        }
