# -*- coding:utf-8 -*-

from __future__ import absolute_import

from .sync.ES2mongodb import EsToMongodb
from .sync.mongodb2json import init_file, user2json
from .sync.ES2csv import EsToCSV
from .sync.csv2ftp import ftp_connect, upload_file
from .sync.config import (FTP_IP, FTP_USER,
                          FTP_PASSWORD, FTP_DIR,
                          CSV_FILE_NAME, CSV_DIR)
from pj.celery import app
from .sync.utils import get_yest_str
import os


@app.task
def es2mongodb():
    # es2mongodb
    info = EsToMongodb()
    now_time_stamp, yest_time_stamp = info.get_time()
    info.deal_data(yest_time_stamp, now_time_stamp)


@app.task
def mongodb2json():
    # mongodb2json
    init_file()
    user2json()


@app.task
def es2csv():
    session_obj = EsToCSV()
    now_time_stamp, yest_time_stamp = session_obj.get_time()
    session_obj.deal_data(yest_time_stamp, now_time_stamp)


@app.task
def csv2ftp():
    ftp = ftp_connect(FTP_IP, FTP_USER, FTP_PASSWORD)

    upload_file(ftp, os.path.join(FTP_DIR, CSV_FILE_NAME.format(get_yest_str()))
                .format(get_yest_str),
                os.path.join(CSV_DIR, CSV_FILE_NAME.format(get_yest_str())))

    ftp.quit()


