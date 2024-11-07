FROM alpine:3.19

RUN apk add --no-cache \
    python3=3.10.11-r0 \
    python3-dev=3.10.11-r0 \
    py3-pip \
    build-base
RUN ln -sf python3 /usr/bin/python
RUN pip3 install --upgrade pip
RUN python --version &&

WORKDIR /app
COPY . /app

