#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from ..user.models import User


def get_credit_rank(num=20):
    '''
    get credit ranking
    '''
    rank_list = User.select().order_by(User.credit.desc()).limit(num)
    return [rank.to_json() for rank in rank_list]
