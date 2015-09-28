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
