FROM python:3.8 as base

RUN apt-get update && apt-get install -y git libpq-dev

WORKDIR /backend

ENV PYTHONBUFFERED=1

RUN python -m venv /venv
RUN python -m pip install poetry

# Copy only poetry files to install
# This will be cached if the requirements don't change
COPY poetry.lock pyproject.toml ./

RUN . /venv/bin/activate && poetry install

# After install copy the rest (separate cache)
COPY . .

RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]