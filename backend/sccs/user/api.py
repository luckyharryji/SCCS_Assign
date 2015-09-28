#!/usr/bin/env python
# -*-coding:utf-8-*-

# api for other service
from peewee import DoesNotExist
from tornado import escape

from .models import User

def create_user(email_prefix,name,password):
    return User.create(email_prefix=email_prefix, name=name, password=password, credit=200)

def get_user_by_name(name):
    '''
    get a sprcific user info
    '''
    return User.get(User.name==name)


def get_user_by_id(user_id):
    '''
    get user by id
    '''
    return User.get(User.id==user_id)


def get_user_rank(user):
    '''
    get the ranking of credit of user
    '''
    return User.select().where(User.credit > user.credit).count() + 1
