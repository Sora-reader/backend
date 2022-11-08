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

.PHONY: help env venv shell shell-sql \
 		jmeter test check fix githooks watch-sass

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
	@$(eval DOTENVS := $(shell test -f "/.dockerenv" || test -f ./.env && echo 'nonzero string'))
	$(if $(DOTENVS),,$(error No .env file found, maybe run "make env"?))

check-venv:
	$(if $(interpreter),, $(error No virtual environment found, run "make venv"))

env: ## Copy env examples and init .envs directory
	@cp .env.example .env

githooks: ## Install git hooks
	@$(interpreter) pre-commit install -t=pre-commit -t=pre-push

venv: ## Create virtual environment and install all dependencies
	@python3 -m pip install pipx && pipx install poetry
	@poetry install && \
	$(print); $(print) "${CYAN}Created venv and installed all dependencies${COFF}"

shell: check-dotenv check-venv ## Run django-extension's shell_plus
	@env IPYTHONDIR="./.ipython" $(interpreter) ./manage.py shell_plus --ipython $(args)

shell-sql: check-dotenv check-venv ## Run shell plus with sql logging
	@make shell args=--print-sql

###############
# Code checks #
###############

jmeter: ## Run jmeter tests
	cd tests
	rm -rf .jmeter_report .jmeter_results
	jmeter -n -t Manga.jmx -l .jmeter_results -e -o .jmeter_report && firefox .jmeter_report/index.html

test: ## Run django tests
	@$(interpreter) pytest

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

#########
# Infra #
#########

webhook-server:
	cd infra
	nohup ./webhook -hooks hooks.yaml -verbose &
