#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import IntegerField, CharField, TextField, DateField, ForeignKeyField

from ..base.models import BaseModel
from ..user.models import User


class Task(BaseModel):
    type = IntegerField(default=0)  # 0-normal 1-hard 2-group
    title = CharField()
    content = TextField(null=True)
    end_date = DateField(null=True)  # end date
    start_date = DateField(null=True)  # after the review, task pushlish date
    pick_date = DateField(null=True)  # when someone begin to do the task
    finish_date = DateField(null=True)  # the end data of a task
    addition = TextField(null=True)
    status = IntegerField(default=2)  # 0-wait to be review，1-did not pass the review，2-wait to be called by someone，3-on working，4-done, wait to be review，5-done，6-close
    creator = ForeignKeyField(User, related_name='tasks')
    reject_reason = CharField(null=True)
    credit = IntegerField(default=0)  # will change when : adding , dit not pass the review and was backed
    max_worker = IntegerField(default=1)  # maxmiun people to do the task
    finish_worker = IntegerField(default=0)  # the number of people in the group task who claim to finish the task

    def to_json(self, simple=False):
        from ..mid_credit.api import get_task_founder

        basic = {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'end_date': self.end_date and self.end_date.strftime('%Y-%m-%d') or None,
            'start_date': self.start_date and self.start_date.strftime('%Y-%m-%d') or None,
            'pick_date': self.pick_date and self.pick_date.strftime('%Y-%m-%d') or None,
            'finish_date': self.finish_date and self.finish_date.strftime('%Y-%m-%d') or None,
            'status': self.status,
            'creator': self.creator.to_json(simple=True),
            'created_date': self.created_date.strftime('%Y-%m-%d'),
            'credit': self.credit,
            'founder': get_task_founder(self, to_json=True),
            'max_worker': self.max_worker,
            'finish_worker': self.finish_worker,
        }
        if self.status in (3, 4, 5):
            # the job was got by people, show people
            basic['worker'] = [t.user.to_json(simple=True) for t in
                               TaskWorker.select().where(TaskWorker.task == self, TaskWorker.status == 0)]
        if self.type == 2:
            # group task, when people involve did not meet the maxmium
            # return the people involved in the group task
            worker = [t.user.to_json(simple=True) for t in
                      TaskWorker.select().where(TaskWorker.task == self, TaskWorker.status == 0)]
            if len(worker) > 0:
                basic['worker'] = worker
        if self.status in (0, 1, 6):
            # wait fot the review
            basic['reject_reason'] = self.reject_reason
        basic['addition'] = self.addition
        return basic


class TaskWorker(BaseModel):
    user = ForeignKeyField(User, related_name='workers')
    task = ForeignKeyField(Task, related_name='workers_tasks')
    status = IntegerField(default=0)  # 0-valid， 1-nonvalid（abandon, remove）

    class Meta:
        indexes = (
            # Specify a unique multi-column index
            (('task', 'user'), True),
        )
