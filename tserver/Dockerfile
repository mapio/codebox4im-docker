FROM dockerfile/python

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN apt-get install -qy libevent-1.4 realpath apt-transport-https

RUN pip install gunicorn gevent flask

RUN rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' tserver

COPY . /tmp/app

RUN cp -r /tmp/app /app && chown -R tserver:tserver /app && rm -rf /tmp/app

WORKDIR /app
USER tserver

CMD [ "/app/bin/gunicorn", "startail" ]

EXPOSE 8000
