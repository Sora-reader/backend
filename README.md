# Backend for manga reader

## Instalation requirements

- PostgreSQL(and `libpq-dev`)
- Python 3.8
- `python-poetry`
- GNU Make (for development, optional)
- Docker

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    make
```

```bash
pip install poetry
sudo snap install docker --classic
# Don't forget to follow post installation steps
# https://docs.docker.com/engine/install/linux-postinstall/
```

## Usage

Use `make` for project management
Run `make` or `make help` to see every command

### Start

1. Create virtual environment `make venv`
2. Generate dotenvs `make env`
3. Run/stop docker `make run`/`make stop`

### Develop

1. Install githooks
2. Activate virtual environment `. venv/bin/activate`
3. Run dev server `make dev`

- Run linters `make check`
- Auto format code `make fix`
