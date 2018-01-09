# -*- coding:utf-8 -*-

from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

CELERY_ROUTES = {
    'pj.tasks.es2mongodb': {'queue': 'es_mongodb', 'routing_key': 'es_mongodb'},
    'pj.tasks.mongodb2json': {'queue': 'mongodb_json', 'routing_key': 'mongodb_json'}
}

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'es_mongodb': {
        'task': 'pj.tasks.es2mongodb',
        'schedule': crontab(hour=10, minute=10)
    },
    'mongodb_json': {
        'task': 'pj.tasks.mongodb2json',
        'schedule': crontab(hour=10, minute=10)
    }
}



BROKER_URL = 'redis://redis:6379/10'
CELERY_RESULT_BACKEND = 'redis://redis:6379/9'
