FROM pcpaquette/tensorflow-serving:20190226

WORKDIR /model/src/model_server

RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install vim
RUN apt-get -y install curl
RUN apt-get -y install htop
RUN apt-get -y install lsof

RUN mkdir /model/src/model_server/bot_neurips2019-sl_model
COPY bot_neurips2019-sl_model /model/src/model_server/bot_neurips2019-sl_model 
COPY run_model_server.sh /model/src/model_server/run_model_server.sh
RUN chmod 777 /model/src/model_server/run_model_server.sh
RUN chmod -R 777 /model/src/model_server/bot_neurips2019-sl_model

# Clone repo
RUN git clone https://github.com/SHADE-AI/diplomacy.git
RUN git clone https://github.com/SHADE-AI/research.git

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
ENV PYTHONIOENCODING=utf-8
ENV LANG=en_CA.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH=/data/env3.7/bin:$PATH

#Default batching parameters, can override with docker run -e 
ENV MAX_BATCH_SIZE=128
ENV BATCH_TIMEOUT_MICROS=250000
ENV MAX_ENQUEUED_BATCHES=1024
ENV NUM_BATCH_THREADS=8
ENV PAD_VARIABLE_LENGTH_INPUTS='true'

WORKDIR /model/src/model_server/research
RUN sed -i 's/gym>/gym=/g'  requirements.txt
RUN pip install -r requirements.txt
COPY run_dipnet.py /model/src/model_server/research/run_dipnet.py
COPY run.sh /model/src/model_server/research/run.sh
RUN chmod 777 /model/src/model_server/research/run_dipnet.py
RUN chmod 777 /model/src/model_server/research/run.sh
ENTRYPOINT ["/model/src/model_server/research/run.sh"]

