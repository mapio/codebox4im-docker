FROM dockerfile/nodejs

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN \
	echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true \
		| debconf-set-selections && \
	add-apt-repository -y ppa:webupd8team/java && \
	apt-get update && \
	apt-get install -y oracle-java7-installer && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk7-installer && \
	adduser --disabled-password --gecos '' esame

RUN npm install -g codebox

RUN mkdir /home/esame/workspace && chown esame:esame /home/esame/workspace

VOLUME [ "/home/esame/workspace" ]

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle
ENV HOME /home/esame

USER esame

EXPOSE 8000

ENTRYPOINT [ "codebox" ]