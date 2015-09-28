#!/usr/bin/env python
# -*-coding:utf-8-*-

from datetime import datetime
from peewee import IntegrityError

from .models import Task, TaskWorker
from ..base.models import db
from ..mid_credit import api as mid_credit_api

def create_task(type, title, content, end_date, addition, credit, creator, max_worker):
    '''
    create a task and minus the credit
    '''
    if creator.credit < credit:
        raise AssertionError('Credit is not enough')
    with db.transaction():
        task = Task.create(type=type, title=title, content=content, end_date=end_date, addition=addition,
                           creator=creator, max_worker=max_worker)
        mid_credit_api.deduct_credit(creator, task, credit)
    return task


def get_task_list(status=None, type=None, order=None, desc=None, page_num=None, page_amount=None):
    '''
    get the list of the task

    status int/None
    None-all，0-wait to be reviewed，1-can not pass，2-wait to be worker，3-on-working，4-done, waiting to be reviewed，5-done，6-close

    type int/None
    None-all，0-normal，1-hard

    order char/None
    credit - order by credit, the other parmeters will order by time

    desc int/None
    0-upper, otherwise down

    page_num int/None from which page(to polish the web loading), default:1
    page_amount int/None number of items show in on page.  >0
    if one of these 2 is None, the will not do page slicing

    no parameter: order by time in desc
    '''
    if status == None:
        # notion the condition when status=0!!
        tasks = Task.select()
    else:
        tasks = Task.select().where(Task.status == status)

    if type != None:
        tasks = tasks.where(Task.type == type)

    if order == 'credit':
        if desc == 0:
            tasks = tasks.order_by(Task.credit)
        else:
            tasks = tasks.order_by(Task.credit.desc())
    else:
        if desc == 0:
            tasks = tasks.order_by(Task.start_date)
        else:
            tasks = tasks.order_by(Task.start_date.desc())
    if page_amount != None and page_num != None and page_amount > 0 and page_num > 0:
        tasks = tasks.paginate(page_num, page_amount)
    return tasks
