#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ..base.handlers import BaseHandler
from . import api as rank_api
from ..utils import get_int_value

class CreditRankHandler(BaseHandler):
    def get(self):
        '''
        get ranking board
        '''
        num = get_int_value(self.get_argument('num',20),20)
        rank = rank_api.get_credit_rank(num)
        rank_text = 1
        rank_true = 1
        last_credit = None
        for r in rank:
            if last_credit == None:
                # first time
                r['rank'] = rank_text
            else:
                if r['credit'] != last_credit:
                    # different credit
                    rank_text = rank_true
            r['rank'] = rank_text
            last_credit = r['credit']
            rank_true += 1
        return self.success_response(rank)
