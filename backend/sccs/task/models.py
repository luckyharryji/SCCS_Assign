#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import IntegerField, CharField, TextField, DateField, ForeignKeyField

from ..base.models import BaseModel
from ..user.models import User


class Task(BaseModel):
    type = IntegerField(default=0)  # 0-普通 1-难题 2-众筹
    title = CharField()
    content = TextField(null=True)
    end_date = DateField(null=True)  # 截止日期
    start_date = DateField(null=True)  # 审核通过的时候算开始时间  Base 里面有一个 create time 是任务提出的时候
    pick_date = DateField(null=True)  # 领取时间
    finish_date = DateField(null=True)  # 完成时间
    addition = TextField(null=True)
    status = IntegerField(default=0)  # 0-等待审核，1-审核不通过，2-等待认领，3-施工中，4-施工完成等待检查，5-完成，6-关闭
    creator = ForeignKeyField(User, related_name='tasks')
    reject_reason = CharField(null=True)
    credit = IntegerField(default=0)  # 每次追加都会修改，退回或完成时也会做一次统计并写入总额
    max_worker = IntegerField(default=1)  # 设置最多认领 task 的人数(仅仅对于众筹类task可以修改)
    finish_worker = IntegerField(default=0)  # 众筹类任务宣布完成的人数

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
            # 被认领了,需要显示被认领的人
            basic['worker'] = [t.user.to_json(simple=True) for t in
                               TaskWorker.select().where(TaskWorker.task == self, TaskWorker.status == 0)]
        if self.type == 2:
            # 众筹类 task 当有人认领，但总认领人数不到提出者设定的最大参与人时，状态仍为 2
            # 返回已经已经认领的几个人
            worker = [t.user.to_json(simple=True) for t in
                      TaskWorker.select().where(TaskWorker.task == self, TaskWorker.status == 0)]
            if len(worker) > 0:
                basic['worker'] = worker
        if self.status in (0, 1, 6):
            # 等待审核，审核不通过，关闭时显示拒绝原因
            basic['reject_reason'] = self.reject_reason
        basic['addition'] = self.addition
        return basic


class TaskWorker(BaseModel):
    user = ForeignKeyField(User, related_name='workers')
    task = ForeignKeyField(Task, related_name='workers_tasks')
    status = IntegerField(default=0)  # 0-有效， 1-无效（放弃任务，或被移除）

    class Meta:
        indexes = (
            # Specify a unique multi-column index
            (('task', 'user'), True),
        )
