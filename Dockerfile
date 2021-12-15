ARG VERSION
FROM python:${VERSION}

RUN pip install tox

ADD . /app
WORKDIR /app

RUN tox -e py
