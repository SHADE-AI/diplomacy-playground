FROM scratch
ENV LANG=en_CA.UTF-8
COPY data /
COPY run.sh /run.sh
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN wineboot --update
ENTRYPOINT ["/bin/bash", "/run.sh"]
