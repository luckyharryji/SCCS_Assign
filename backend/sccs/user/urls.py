#!/usr/bin/env python
# -*-coding:utf-8-*-
from . import handlers

urls = [
    (r'/current',handlers.CurrentUserHandler),
    (r'/(\d+)/people/credit',handlers.ShowPeopleCreditHandler),
]
