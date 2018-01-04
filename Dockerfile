FROM python:3.6.3

ADD ./src /app/src
ADD requirements.txt /app/requirements.txt
ADD config.py /app/src/main/python/sync/config.py

workdir /app/
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

workdir /app/src/main/python/sync