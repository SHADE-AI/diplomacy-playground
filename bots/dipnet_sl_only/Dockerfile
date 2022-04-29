FROM pcpaquette/tensorflow-serving:20190226

WORKDIR /model/src/model_server

RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install vim
RUN apt-get -y install curl
RUN apt-get -y install htop
RUN apt-get -y install lsof


# Clone repo
RUN git clone https://github.com/SHADE-AI/diplomacy.git
WORKDIR diplomacy
RUN git checkout development
RUN pip install -r requirements.txt

WORKDIR /model/src/model_server
RUN git clone https://github.com/SHADE-AI/research.git

WORKDIR /model/src/model_server/research
RUN git checkout tacc_hpc
RUN sed -i 's/gym>/gym=/g'  requirements.txt

RUN pip install -r requirements.txt
COPY run_dipnet.py /model/src/model_server/research/run_dipnet.py
RUN chmod 777 /model/src/model_server/research/run_dipnet.py
ENTRYPOINT ["python", "/model/src/model_server/research/run_dipnet.py"]

