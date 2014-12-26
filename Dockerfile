FROM dockerfile/nodejs

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN \
	echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections &&\
	echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections &&\
	add-apt-repository -y ppa:webupd8team/java &&\
	apt-get -qy update &&\
	apt-get -qy install oracle-java7-installer

RUN npm install -g codebox

EXPOSE 8000

ENTRYPOINT [ "codebox" ]
