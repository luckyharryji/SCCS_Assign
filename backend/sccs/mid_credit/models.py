#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import IntegerField, ForeignKeyField, BooleanField, CharField

from ..base.models import BaseModel
from ..user.models import User
from ..task.models import Task

class MidCredit(BaseModel):
    user = ForeignKeyField(User,related_name='owners')
    task = ForeignKeyField(Task,related_name='tasks')
    credit = IntegerField()
    credit_text = IntegerField()

    class Meta:
        indexes = (
            # Specify a unique multi-column index
            (('task', 'user'), True),
        )

    def to_json(self,simple=False):
        basic = {
            'user': self.user.to_json(simple=True),
            'task': self.task.to_json(simple=True),
            'credit': self.credit,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return basic


class CreditLog(BaseModel):
    user = ForeignKeyField(User,related_name='credit logs')
    minus = BooleanField(default=False)
    amount = IntegerField()
    reason = CharField(default='')

    def to_json(self,simple=True):
        return {
            'user': self.user.id,
            'minus': self.minus,
            'amount': self.amount,
            'reason': self.reason,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }
