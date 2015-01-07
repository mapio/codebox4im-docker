FROM dockerfile/python

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN apt-get install -qy libevent-1.4 realpath apt-transport-https

RUN echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 \
		--recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9

RUN apt-get update

RUN apt-get install -y lxc-docker

RUN pip install gunicorn gevent flask

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD [ "/app/bin/gunicorn", "startail" ]

EXPOSE 8000
