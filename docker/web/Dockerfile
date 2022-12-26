FROM python:3.10-slim as base

RUN apt-get update && apt-get install -y \
    sudo curl gcc g++ \
    libffi-dev libpq-dev \
    postgresql-client

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG USERNAME=sora
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME
ENV HOME="/home/$USERNAME"
ENV PATH="${PATH}:$HOME/.local/bin"

RUN pip install --upgrade pip pipx && pipx install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .
RUN sudo chown -R $USERNAME:$USERNAME .

RUN SECRET_KEY=1 poetry run python manage.py collectstatic --noinput

RUN chmod +x scripts/entrypoint.sh
CMD ["./scripts/entrypoint.sh"]

EXPOSE "$PORT"
EXPOSE 1233