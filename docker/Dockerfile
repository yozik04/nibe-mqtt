ARG BUILD_FROM=python:3-alpine
FROM $BUILD_FROM

COPY docker/ensure_pip3.sh /ensure_pip3.sh
RUN /ensure_pip3.sh

COPY . /src
COPY config_example.yaml /default/config_example.yaml
COPY docker/run.sh /run.sh

EXPOSE 9999/udp

RUN pip3 install /src && rm -fr /src

CMD [ "/run.sh" ]