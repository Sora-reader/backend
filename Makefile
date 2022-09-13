##########
# Config #
##########
SHELL = bash
print = echo -e

CYAN ?= \033[0;36m
RED ?= \033[0;31m
COFF ?= \033[0m
COMPOSE = docker-compose.yml
port ?= 8000

.PHONY: help env venv shell dev \
 		check fix

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-30s$(COFF) %s\n", $$1, $$2}'

###########
# Project #
###########

interpreter := $(shell poetry env info > /dev/null 2>&1 && echo "poetry run")
extract_ignores = $(shell awk '/.*.py/{split($$1,a,":"); print a[1]}' .flake8 | tr '\n' ',')

check-dotenv:
	@$(eval DOTENVS := $(shell test -n "$$SECRET_KEY" || (test -f ./.envs/docker.env && test -f ./.envs/local.env) && echo 'nonzero string'))
	$(if $(DOTENVS),,$(error No .env files found, maybe run "make env"?))

check-venv:
	$(if $(interpreter),, $(error No virtual environment found, run "make venv"))

env: ## Copy env examples and init .envs directory
	@mkdir -p .envs
	@for file in .envs.example/*; do
			[[ "$$file" != *deployment* ]] && \
			echo "$$file" ".envs/$$(basename ".envs/$${file%%.example}")"
	@done
	@$(print) "${CYAN}Done${COFF}"

githooks:
	@$(interpreter) pre-commit install -t=pre-commit -t=pre-push

venv: ## Create virtual environment and install all dependencies
	@python3.8 -m pip install poetry==1.1.4
	@poetry install && \
	$(print); $(print) "${CYAN}Created venv and installed all dependencies${COFF}"

shell: check-dotenv check-venv ## Run django-extension's shell_plus
	@$(interpreter) ./manage.py shell_plus --ipython --print-sql -- -i -c """
	from rich import pretty, inspect
	from django.db import connection
	from django.db.models import *
	from django.db.models.functions import *
	from django.contrib.postgres.aggregates import ArrayAgg
	pretty.install()
	"""

shell-sql: check-dotenv check-venv ## Run django-extension's shell_plus
	@$(interpreter) ./manage.py shell_plus --ipython --print-sql -- -i -c """from rich import pretty, inspect
	pretty.install()
	"""

runserver: check-dotenv check-venv  ## Run dev server on port 8000, or specify with "make dev port=1234"
	@. ./.envs/local.env && if [ "$(DEBUG)" = 0 ]; then ./manage.py collectstatic --noinput --clear; fi
	@$(interpreter) ./manage.py migrate --noinput
	@$(interpreter) ./manage.py runserver 0.0.0.0:$(port)
	@$(print) "${CYAN}Backend is running on localhost:$(port)${COFF}"

development: ## run dev docker
	@# Force recreate to reload NGINX config
	@# as it won't rebuild because the config is passed as a volume
	@docker-compose -f ${COMPOSE} up -d --build --force-recreate
	@$(print) "${CYAN}Backend is running on http://localhost:8880${COFF}"

stop: ## stop docker containers
	@docker-compose -f ${COMPOSE} down

clear: ## down containers and clear volumes
	@docker-compose -f ${COMPOSE} down --volumes

###############
# Code checks #
###############

jmeter: ## Run jmeter tests
	cd tests
	rm -rf .jmeter_report .jmeter_results
	jmeter -n -t Manga.jmx -l .jmeter_results -e -o .jmeter_results && firefox .jmeter_report/index.html

check: check-venv ## Run linters
	@$(print) "flake8"
	@$(print) "======"
	@$(interpreter) flake8 || exit 1
	@$(print) "OK"
	@$(print);
	@$(print) "black"
	@$(print) "======"
	@$(interpreter) black --check . || exit 1
	@$(print);
	@$(print) "isort"
	@$(print) "======"
	@$(interpreter) isort --check-only .

# Fix $(filename) with autoflake ignoring extracted files from .flake8
# You probably shouldn't use it manually, so it's not documented in help
autoflake_fix:
	@$(interpreter) autoflake -i --remove-all-unused-imports --exclude $(extract_ignores) $(filename)

fix: check-venv ## Run code formatters
	@$(print) "autoflake"
	@$(print) "========="
	@$(interpreter) autoflake -ri --remove-all-unused-imports --exclude $(extract_ignores) .
	@$(print) "black"
	@$(print) "====="
	@$(interpreter) black .
	@$(print);
	@$(print) "isort"
	@$(print) "====="
	@$(interpreter) isort .

watch-sass:
	@/bin/find -type d -name 'scss' -not -path '*/staticfiles/*' | xargs -P 0 -l -i bash -c 'sass --watch "$$1:$${1:0:-5}/css"' - '{}'
