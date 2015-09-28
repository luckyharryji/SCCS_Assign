#!/usr/bin/env python
# -*-coding:utf-8-*-

from .models import Comment


def get_comment_by_task(t):
    '''
    get comments by task obj
    returns QuerySet of Comment, order by time asc
    '''
    return Comment.select().where(Comment.task==t).order_by(Comment.created_date.asc())

def add_comment(t,user,content,reply):
    '''
    add comment
    '''
    c = Comment.create(task=t,user=user,content=content,reply=reply)
    return c
