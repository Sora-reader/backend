# Backend for manga reader

## Instalation requirements

- PostgreSQL(and `libpq-dev`)
- Python 3.8+
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
    - To use installed dependencies prepend commands with `poetry run ...` (e.x. `poetry run ./manage.py makemigrations`). This will allow you to use your venv without actiavating it
    - Activate poetry-created venv with `. "$(poetry env info --path)/bin/activate"`. Show poetry's venv info with `poetry env info`
3. Generate dotenvs `make env`

### Development

1. Install githooks
2. Run/stop docker `make development`/`make stop`
3. Or run django dev server `make runserver`

- Run linters `make check`
- Auto format code `make fix`
- Clear database volume with `make clear`
