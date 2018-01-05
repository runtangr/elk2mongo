# -*- coding:utf-8 -*-

from __future__ import absolute_import

from celery import Celery

# set redis 100 as broker
app = Celery('pj',
             include=['pj.tasks'])

app.config_from_object('pj.celery_config')


if __name__ == '__main__':
    app.start()
