FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Install postgres client
RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
RUN apk add --update --no-cache --virtual .tmp-build-deps \
	gcc libc-dev linux-headers postgresql-dev libffi-dev libjpeg
RUN pip install -r /requirements.txt


RUN apk del .tmp-build-deps

RUN mkdir /social_network
WORKDIR /social_network
COPY ./ ./


RUN adduser -D river


USER river