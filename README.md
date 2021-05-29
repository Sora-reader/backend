# Backend for manga reader

## Instalation requirements

- PostgreSQL(and `libpq-dev`)
- Python 3.8+
- `python-poetry`
- `pre-commit` for git hooks
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

**[Read this](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) to understand `poetry shell`**

### Start

1. Create virtual environment `make venv`
    - To activate freshly created environment run `. "$(poetry env info -p)/bin/activate`.
    You can also use `poetry shell`, but it's buggy
    - Show poetry's venv info with `poetry env info`
2. Install githooks with `make githooks`
3. Generate dotenvs `make env`

### Development

1. Install githooks
2. Run/stop docker `make development`/`make stop`
3. Or run django dev server `make runserver`

- Run linters `make check`
- Auto format code `make fix`
- Clear database volume with `make clear`
