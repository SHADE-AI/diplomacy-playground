FROM ubuntu:18.04

ENV LANG=en_CA.UTF-8

RUN apt-get -y update
RUN apt-get install -y software-properties-common wget unzip apt-transport-https
RUN echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | debconf-set-selections
RUN dpkg --add-architecture i386
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 76F1A20FF987672F
RUN apt-add-repository https://dl.winehq.org/wine-builds/ubuntu/
RUN apt-get update -y
RUN apt-get install -y --allow-unauthenticated winehq-stable xvfb x11-xserver-utils

RUN apt-get clean ; apt-get autoclean; rm -rf /var/lib/apt/lists/*

# Installing Albert
RUN mkdir -p /data/albert
RUN cd /data/albert; wget -nv https://storage.googleapis.com/ppaquette-diplomacy/files/bots/albert.zip; unzip albert.zip; rm albert.zip

# Install Dumbbot
RUN mkdir -p /data/dumbbot; cd /data/dumbbot; wget -nv https://storage.googleapis.com/ppaquette-diplomacy/files/bots/dumbbot.zip; unzip dumbbot.zip; rm dumbbot.zip

# Cleaning up
RUN chmod -R 777 /data
ADD run.sh /run.sh

CMD ["bash", "./run.sh"]
