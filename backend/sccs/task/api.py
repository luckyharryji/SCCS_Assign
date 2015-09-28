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


def add_task_founder(founder, task, credit):
    with db.transaction():
        mid_credit_api.deduct_credit(founder, task, credit)
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


def get_task_by_id(task_id):
    return Task.get(id=int(task_id))

def update_task_status(t, status):
    '''
    '''
    with db.transaction():
        if status == 1 or status == 6:
            mid_credit_api.return_credit(t)
        elif status == 5:
            mid_credit_api.finish_credit(t)
            t.finish_date = datetime.now()
        t.status = status
        t.save()
    return t

# task worker
def get_task_worker(t):
    '''
    returns a python list of who is doing the task
    '''
    return [tw.user for tw in TaskWorker.select().where(TaskWorker.task == t, TaskWorker.status == 0)]


def update_task_content(t, title, content, end_date, addition):
    '''
    '''
    t.title = title
    t.content = content
    t.end_date = end_date
    t.addition = addition
    t.save()
    return t


def add_task_worker(t, user):
    '''
    return queue of the helper of the task
    '''
    with db.transaction():
        try:
            tw = TaskWorker.create(user=user, task=t)
        except IntegrityError:
            tw = TaskWorker.get(user=user, task=t)
            tw.status = 0
            tw.save()
    return get_task_worker(t)


def add_finish_worker(t):
    '''
    for group type task
    '''
    with db.transaction():
        t.finish_worker += 1
        t.save()
    return t

def remove_task_worker(t, user):
    '''
    '''
    try:
        tw = TaskWorker.get(user=user, task=t)
        tw.status = 1
        tw.save()
    except TaskWorker.DoesNotExist:
        pass
    finally:
        return get_task_worker(t)


def get_task_by_user(type, login_user, return_count=False):
    '''
    '''
    if type == 0:
        tasks = [t for t in Task.select().where(Task.creator == login_user)]
    elif type == 1:
        tws = TaskWorker.select().where(TaskWorker.user == login_user, TaskWorker.status == 0)
        tasks = [tw.task for tw in tws if tw.task.status == 3 or tw.task.status == 4]
    elif type == 2:
        tws = TaskWorker.select().where(TaskWorker.user == login_user, TaskWorker.status == 0)
        tasks = [tw.task for tw in tws if tw.task.status == 5]
    elif type == 3:
        related_tasks = mid_credit_api.get_tasks_from_user(login_user)
        tasks = [t for t in related_tasks if t.status in (2, 3, 4, 5) and t.creator != login_user]
    elif type == 4:
        tasks = [t for t in Task.select().where(Task.status == 4, Task.creator == login_user)]
    else:
        return None
    if return_count:
        return len(tasks)
    else:
        return tasks
