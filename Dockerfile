FROM python:3.8-slim as base

# Install chrome wed driver
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

RUN apt-get install -y \
    gcc g++ \
    libffi-dev \
    libpq-dev \
    '^postgresql-client-.+$' \
    gettext git make

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
