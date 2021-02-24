FROM python:3.8 as base

RUN apt-get update && apt-get install -y git

WORKDIR /backend

ENV PYTHONBUFFERED=1

COPY . .

RUN python -m venv /venv

RUN python -m pip install poetry

RUN . /venv/bin/activate && poetry install

COPY docker-entrypoint.sh manage.py ./

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]