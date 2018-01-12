# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os
import datetime
from .config import (FTP_DIR, CSV_FILE_NAME,
                     FTP_IP, FTP_USER,
                     FTP_PASSWORD, CSV_DIR)
from .utils import get_yest_str

from ftplib import FTP


def ftp_connect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


# 从本地上传文件到ftp
def upload_file(ftp_fd, remotepath, localpath):
    buf_size = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, buf_size)
    ftp_fd.set_debuglevel(0)
    fp.close()

if __name__ == "__main__":

    ftp = ftp_connect(FTP_IP, FTP_USER, FTP_PASSWORD)

    upload_file(ftp, os.path.join(FTP_DIR, CSV_FILE_NAME.format(get_yest_str()))
                .format(get_yest_str),
                os.path.join(CSV_DIR, CSV_FILE_NAME.format(get_yest_str())))

    ftp.quit()
