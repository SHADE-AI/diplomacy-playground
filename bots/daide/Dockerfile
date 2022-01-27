# 20.04 maps to 20.04.x which is a LTS release
FROM ubuntu:20.04

ENV LANG=en_CA.UTF-8

# Skip interactive prompts
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y git cmake build-essential

RUN apt-get clean ; apt-get autoclean; rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
RUN git clone https://github.com/diplomacy/daide-client.git
WORKDIR /code/daide-client
RUN cmake .

COPY run.sh /code/run.sh

ENTRYPOINT [ "bash", "/code/run.sh" ]
