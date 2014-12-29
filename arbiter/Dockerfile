FROM dockerfile/python

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN \
	apt-get update && apt-get install -qy libevent-1.4 realpath docker.io && \
	pip install gunicorn gevent flask && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD . /app

CMD [ "/app/bin/gunicorn", "startail" ]

EXPOSE 8000
