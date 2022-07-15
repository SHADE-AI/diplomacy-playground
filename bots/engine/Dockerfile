FROM python:3.7-slim

ARG GIT_REPO=https://github.com/SHADE-AI/diplomacy.git
ARG GIT_BRANCH=development


RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install vim
RUN apt-get -y install curl
RUN apt-get -y install htop
RUN apt-get -y install lsof

#set default environment variables
ENV DAIDE_PORT_RANGE=8434:8600
ENV DIPLOMACY_ADMIN_PASSWORD=password
ENV SERVER_PORT=8432
ENV LOGFILE=diplomacy.server.log
ENV SERVER_DIR=/code
ENV PYTHONPATH=/code/diplomacy:/code/diplomacy-plaground

# Get diplomacy and diplomacy-playground repo
# allow user to set SERVER_DIR via -e (docker) or --env (singularity)
WORKDIR $SERVER_DIR
RUN git clone ${GIT_REPO}
WORKDIR ${SERVER_DIR}/diplomacy
RUN git checkout ${GIT_BRANCH} && pip install --upgrade .

WORKDIR $SERVER_DIR
RUN git clone https://github.com/SHADE-AI/diplomacy-playground.git
WORKDIR ${SERVER_DIR}/diplomacy-playground
RUN git checkout dev && pip install hashids


#WORKDIR /code/diplomacy/diplomacy/maps
#RUN find . -type f ! \( -name 'standard.map' -o -name '*init*'  \) -delete

#to speed up server launch, we inject pre-computed convoy paths into container
WORKDIR ${SERVER_DIR}/maps
COPY convoy_paths_cache.pkl .

#to speed up server launch, we inject initilized server.json (this includes pre-computed variables for various Maps)
#at run time, server.json will be copied to $SERVER_DIR/data in start.sh script, which is where the engine expects it
WORKDIR ${SERVER_DIR}/tmp
COPY server.json .

WORKDIR ${SERVER_DIR}
COPY start.sh .
RUN chmod 777 start.sh

WORKDIR ${SERVER_DIR}/data
RUN mkdir -p games
#COPY server.json .

WORKDIR /
RUN mkdir -p ${SERVER_DIR}/logs && touch ${SERVER_DIR}/logs/$LOGFILE


#COPY start.sh .
#CMD ["/bin/sh", "-c", "python -m diplomacy.server.run >> /logs/diplomacy_server_run.log 2>&1"]
#CMD ["sh","start.sh"]
#CMD ["/bin/sh","-c","python -m diplomacy.server.run --server_dir $SERVER_DIR"]
ENTRYPOINT ["/bin/sh","-c","${SERVER_DIR}/start.sh $SERVER_DIR $LOGFILE"]
