FROM dockerfile/nodejs

MAINTAINER Massimo Santini "santini@di.unimi.it"

ENV DEBIAN_FRONTEND noninteractive

RUN add-apt-repository -y ppa:webupd8team/java

RUN apt-get update

RUN	echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true \
		| debconf-set-selections && \
	 apt-get install -y oracle-java7-installer && \
	 rm -rf /var/cache/oracle-jdk7-installer

RUN rm -rf /var/lib/apt/lists/*

RUN npm install -g codebox

RUN adduser --disabled-password --gecos '' esame

RUN mkdir /home/esame/workspace

ADD ./bashrc /home/esame/.bashrc
ADD ./profile /home/esame/.profile

RUN chown -R esame:esame /home/esame

VOLUME [ "/home/esame/workspace" ]

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle
ENV HOME /home/esame

USER esame

EXPOSE 8000

ENTRYPOINT [ "codebox" ]
