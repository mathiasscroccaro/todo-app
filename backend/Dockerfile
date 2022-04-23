FROM python:3

ENV PYTHONUNBUFFERED=1

RUN mkdir /django-app
COPY ./requirements.txt /django-app/

WORKDIR /django-app
RUN pip install -r requirements.txt

