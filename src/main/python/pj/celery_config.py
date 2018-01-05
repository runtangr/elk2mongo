# -*- coding:utf-8 -*-

from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

CELERY_ROUTES = {
    'pj.tasks.es2mongodb': {'queue': 'es_mongodb', 'routing_key': 'es_mongodb'}
}

CELERYBEAT_SCHEDULE = {
    'es_mongodb': {
        'task': 'pj.tasks.es2mongodb',
        'schedule': crontab(hour=8, minute=30)
    }
}

CELERY_TIMEZONE = 'Asia/Shanghai'

BROKER_URL = 'redis://redis:6379/10'
CELERY_RESULT_BACKEND = 'redis://redis:6379/9'
