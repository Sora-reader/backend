FROM python:3.8-slim as base

RUN apt-get update && apt-get install -y \
    gcc g++ \
    libffi-dev \
    libpq-dev \
    '^postgresql-client-.+$' \
    gettext git

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . .

RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
