FROM python:3.7

ENV DIPLO_GAMEID=
ENV DIPLO_DAIDE_PORT=
ENV DIPLO_POWER=
ENV DIPLO_USERNAME=
ENV DIPLO_PASSWORD=
ENV DIPLO_HOST=locahost
ENV DIPLO_PORT=8432

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /code
ADD pyrandom.py /code/pyrandom.py

ENTRYPOINT [ "python",  "/code/pyrandom.py"]

