#!/usr/bin/env python
# -*-coding:utf-8-*-
from peewee import CharField,IntegerField

from ..base.models import BaseModel

class User(BaseModel):
    email_prefix = CharField(unique=True)
    name = CharField()
    credit = IntegerField(default=0)
    img = CharField(null=True)
    password = CharField()

    def to_json(self,simple=False):
        result = {
            'id':self.id,
            'email_prefix':self.email_prefix,
            'credit':self.credit,
            'name':self.name,
            'img':self.img,
        }
        return result
