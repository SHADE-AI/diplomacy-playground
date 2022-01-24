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
ADD random_bot.py /code/random_bot.py

CMD [ "python",  "/code/random_bot.py"]

