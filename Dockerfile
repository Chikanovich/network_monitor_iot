FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# upgrade pip
RUN pip install pip -U

# install dependencies
ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD . /code

RUN apt-get update
RUN apt-get install cron nmap python3-dev default-libmysqlclient-dev -y