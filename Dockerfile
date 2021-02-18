FROM python:3.8 as base

RUN apt-get update && apt-get install -y git

RUN mkdir -p /backend
WORKDIR /backend

ENV PYTHONBUFFERED=1

COPY . /backend

RUN python -m venv /venv
RUN . /venv/bin/activate 
RUN python -m pip install poetry

RUN python -m poetry install
