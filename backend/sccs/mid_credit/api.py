#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import IntegrityError
from .models import MidCredit, CreditLog
from ..base.models import db
from ..task.models import TaskWorker


def deduct_credit(user, task, credit):
    '''
    deduce the task provider's credit and save to system mid account
    '''
    if user.credit >= credit:
        try:
            with db.transaction():
                MidCredit.create(user=user, task=task, credit=credit, credit_text=credit)
                change_user_credit(user, True, credit, u'need to ：%s' % task.title)
        except IntegrityError:
            # `username` is a unique column, so this username already exists,
            # making it safe to call .get().
            with db.transaction():
                mid = MidCredit.get(user=user, task=task)
                mid.credit = mid.credit + credit
                mid.credit_text = mid.credit
                mid.save()
                change_user_credit(user, True, credit, u'need to ：%s' % task.title)
        finally:
            task.credit = get_total_credit(task)
            task.save()
            return True
    else:
        raise AssertionError('Credit is not enough')



def return_credit(task):
    '''
    give the credit back
    '''
    mids = MidCredit.select().where(MidCredit.task == task)
    total_credit = 0
    with db.transaction():
        for m in mids:
            if m.credit > 0:
                total_credit = total_credit + m.credit
                change_user_credit(m.user, False, m.credit, u'close need ：%s' % task.title)
                m.credit = 0
                m.save()
        if total_credit > 0:
            task.credit = total_credit
            task.save()
    return True


def finish_credit(task):
    '''
    give out the credit when finishing a task
    '''
    mids = MidCredit.select().where(MidCredit.task == task)
    total_credit = 0
    with db.transaction():
        for m in mids:
            total_credit = total_credit + m.credit
            m.credit = 0
            m.save()
        workers = [tw.user for tw in TaskWorker.select().where(TaskWorker.task == task, TaskWorker.status == 0)]
        worker_num = len(workers)
        balance = int(total_credit) / int(worker_num)
        for w in workers:
            change_user_credit(w, False, balance, u'finish：%s' % task.title)
    return True


def change_user_credit(u, minus, amount, reason):
    if minus == True:
        u.credit -= int(amount)
        u.save()
    elif minus == False:
        u.credit += int(amount)
        u.save()
    else:
        return False
    CreditLog.create(user=u, minus=minus, amount=amount, reason=reason)
    return True


def get_total_credit(task):
    '''
    the total credit of a task
    '''
    mid_list = MidCredit.select().where(MidCredit.task == task)
    total = 0
    for m in mid_list:
        total = total + m.credit
    return total


def get_task_founder(task, to_json=False):
    '''
    credit provider of the task

    [{"user":{...},"credit":100},{...}]
    '''
    founder = MidCredit.select().where(MidCredit.task == task)
    result = list()
    for f in founder:
        if to_json:
            result.append({'user': f.user.to_json(), 'credit': f.credit_text})
        else:
            result.append({'user': f.user, 'credit': f.credit_text})
    return result


def get_tasks_from_user(user):
    '''
    the task that user give credit to

    Python List of task Query will be returned
    '''
    return [t.task for t in MidCredit.select().where(MidCredit.user == user)]


def get_mid_credit_from_user(user):
    '''
    the credit of the user still in the mid credit
    '''
    return [t for t in MidCredit.select().where(MidCredit.user == user)]


# credit log
def get_credit_log_by_user(user, num=20):
    '''
    the credit history of the user
    '''
    logs = CreditLog.select().where(CreditLog.user == user).order_by(CreditLog.created_date.desc())
    if num == 'all':
        return logs
    else:
        return logs.limit(num)
