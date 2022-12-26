# Sora reader backend

## UI Preview

![image](https://user-images.githubusercontent.com/18076967/131153731-0196375e-b650-4b0f-b188-f20b2eba37f1.png)


## Notes

- Postgres 15+ is mandatory for NULLS NOT DISTINCT indexes
- [webhook-server](https://github.com/adnanh/webhook/releases)

## Installation requirements

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
