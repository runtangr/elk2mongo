FROM python:3.6.3

ADD ./src /app/src
ADD requirements.txt /app/requirements.txt

workdir /app/
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

workdir /app/src/main/python/