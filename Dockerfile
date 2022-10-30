FROM python:3
USER root
RUN apt-get update
RUN apt-get -y install locales-all
RUN apt-get install -y vim less

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN mkdir -p /root/src
COPY requirements.txt /root/src
WORKDIR /root/src

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir pandas --no-build-isolation
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt