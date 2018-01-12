# -*- coding:utf-8 -*-

from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

CELERY_ROUTES = {
    'pj.tasks.es2mongodb': {'queue': 'es_mongodb', 'routing_key': 'es_mongodb'},
    'pj.tasks.mongodb2json': {'queue': 'mongodb_json', 'routing_key': 'mongodb_json'},
    'pj.tasks.es2csv': {'queue': 'es_csv', 'routing_key': 'es_csv'},
    'pj.tasks.csv2ftp': {'queue': 'csv_ftp', 'routing_key': 'csv_ftp'}

}
# i don't know why i use this configuration, timezone is utc
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYBEAT_SCHEDULE = {
    'es_mongodb': {
        'task': 'pj.tasks.es2mongodb',
        'schedule': crontab(hour=8, minute=41)
    },
    'mongodb_json': {
        'task': 'pj.tasks.mongodb2json',
        'schedule': crontab(hour=8, minute=45)
    },
    'es_csv': {
        'task': 'pj.tasks.es2csv',
        'schedule': crontab(hour=8, minute=50)
    },
    'csv_ftp': {
        'task': 'pj.tasks.csv2ftp',
        'schedule': crontab(hour=8, minute=55)
    }
}


BROKER_URL = 'redis://redis:6379/10'
CELERY_RESULT_BACKEND = 'redis://redis:6379/9'
