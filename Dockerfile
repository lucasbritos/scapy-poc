FROM python:3.8

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt -y update && apt -y upgrade
RUN apt-get -y install binutils

COPY requirements.txt requirements.txt
COPY src src
RUN mkdir build_output
RUN pip install -r requirements.txt