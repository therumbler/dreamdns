FROM python:3.8

RUN mkdir /app
WORKDIR /app

COPY * ./

ENTRYPOINT python main.py
