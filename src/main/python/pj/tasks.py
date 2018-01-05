# -*- coding:utf-8 -*-

from __future__ import absolute_import

from .sync.ES2mongodb import EsToMongodb
from .sync.mongodb2json import init_file, user2json
from pj.celery import app


@app.task
def es2mongodb():
    # es2mongodb
    info = EsToMongodb()
    now_time_stamp, yest_time_stamp = info.get_time()
    info.deal_data(yest_time_stamp, now_time_stamp)

    # mongodb2json
    init_file()
    user2json()



