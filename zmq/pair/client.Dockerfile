# FROM python:3.9
FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=1
# RUN apt-get update -qq \
#     && apt-get install -y -qq --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*
RUN apk add --no-cache g++ libzmq zeromq-dev linux-headers py3-pip

WORKDIR /backend
RUN pip3 install pyzmq
COPY client.py ./client.py
# EXPOSE 5556
CMD python3 client.py