FROM python:3.7

ARG GIT_REPO=https://github.com/SHADE-AI/diplomacy.git
ARG GIT_BRANCH=development

ENV DAIDE_PORT_RANGE=8434:8600
ENV DIPLOMACY_ADMIN_PASSWORD=password
ENV SERVER_PORT=8432
ENV PYTHONPATH=/code/diplomacy/

# RUN pip install diplomacy <- public release version
WORKDIR /code
# Install SHADE-AI's development version
RUN git clone ${GIT_REPO}
WORKDIR /code/diplomacy
RUN git checkout ${GIT_BRANCH}

#install SHADE-AI's research repo
WORKDIR /code
RUN git clone https://github.com/SHADE-AI/research.git

WORKDIR /code/research
RUN sed -i 's/gym>/gym=/g'  requirements.txt
RUN pip install -r requirements.txt

COPY run_dumbbot.py /code/research/run_dumbbot.py
COPY run.sh /code/research/run.sh
RUN chmod 777 run.sh
ENTRYPOINT ["/code/research/run.sh"]

