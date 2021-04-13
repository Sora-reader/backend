##########
# Config #
##########

.PHONY: help env venv githooks shell run \
 		test check fix \
		run stop test-ignore show-build-files

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###########
# Project #
###########

interpreter := $(shell (poetry env info --path > /dev/null 2>&1 && echo "poetry run") || ([ -n "$(VIRTUAL_ENV)" ] && echo "python") )

check-dotenv:
	@$(eval DOTENVS := $(shell test -f ./.envs/dev.env && test -f ./.envs/local.env && echo 'nonzero string'))
	$(if $(DOTENVS),,$(error No .env files found, maybe run "make env"?))

check-venv:
	$(if $(interpreter),, $(error No virtual environment found, either run "make venv" or activate existing))

env: ## Copy env examples and init .envs directory
	@mkdir -p .envs
	@cp -R .envs.example/. .envs
	@for file in .envs/*.example; do \
		if [ -f "$${file%%.example}" ]; then
			rm "$$file"
		else
			mv --backup=numbered "$$file" "$${file%%.example}"
		fi;
	@done
	@echo "Generated .env files to .envs/"

venv: ## Create virtual environment and install all dependencies
	@python3.8 -m pip install poetry==1.1.4
	@poetry install && \
	echo; echo "Created .venv/ and installed all dependencies"


githooks: check-venv  ## Install git hooks
	@$(interpreter) pre-commit install -t=pre-commit

shell: check-dotenv check-venv ## Run django-extension's shell_plus, enable rich pretty printing and import 'inspect'
	@$(interpreter) ./manage.py shell_plus --ipython -- -i -c """from rich import pretty, inspect
	pretty.install()
	"""

dev: check-dotenv check-venv  ## Run dev server on port 8000, or specify with "make dev port=1234"
	@. ./.envs/local.env && if [ "$(DEBUG)" = 0 ]; then $(interpreter) ./manage.py collectstatic --noinput --clear; fi
	@$(interpreter) ./manage.py migrate --noinput
	@$(interpreter) ./manage.py runserver $(port)

###############
# Code checks #
###############

test: check-venv ## Test code with pytest
	@echo "pytest"
	@echo "======"
	@$(interpreter) pytest

check: check-venv ## Run linters
	@echo "flake8"
	@echo "======"
	@$(interpreter) flake8 || exit 1
	@echo "OK"
	@echo;
	@echo "black"
	@echo "======"
	@$(interpreter) black --check . || exit 1
	@echo;
	@echo "isort"
	@echo "======"
	@$(interpreter) isort --check-only .

fix: check-venv ## Run code formatters
	@echo "black"
	@echo "====="
	@$(interpreter) black .
	@echo;
	@echo "isort"
	@echo "====="
	@$(interpreter) isort .

##########
# Docker #
##########

run: check-dotenv ## Run production containers
	@docker-compose up -d --build || exit 1
	@echo;
	@echo "Backend is running on http://localhost:5500, the db is available at localhost:5502"

stop: ## Stop production containers
	@docker-compose down

show-build-files: ## Test local .dockerignore, output local files after build
	@docker build -t test-dockerfile . && \
	docker run --rm --entrypoint=/bin/sh test-dockerfile -c find .

test-ignore: ## Build Dockerfile and output WORKDIR files
	@cat <<EOF > Dockerfile.build-context
	@FROM busybox
	@COPY $(COMPOSE_DIR) /build-context
	@WORKDIR /build-context
	@CMD find .
	@EOF
	@docker build -f Dockerfile.build-context -t build-context .
	@docker run --rm -it build-context
	@rm Dockerfile.build-context
