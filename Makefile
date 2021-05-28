##########
# Config #
##########

CYAN ?= \033[0;36m
RED ?= \033[0;31m
COFF ?= \033[0m
COMPOSE=docker-compose.yml
port?=8000

.PHONY: help env venv shell dev \
 		check fix

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-30s$(COFF) %s\n", $$1, $$2}'

###########
# Project #
###########

interpreter_found := $(shell [ -n "$$VIRTUAL_ENV" ] && echo "yes")

check-dotenv:
	@$(eval DOTENVS := $(shell test -f ./.envs/docker.env && test -f ./.envs/local.env && echo 'nonzero string'))
	$(if $(DOTENVS),,$(error No .env files found, maybe run "make env"?))

check-venv:
	$(if $(interpreter_found),, $(error No virtual environment found, either run "make venv" or "poetry shell"))

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
	@echo "${CYAN}Done${COFF}"

githooks:
	@pre-commit install -t=pre-commit -t=pre-push

venv: ## Create virtual environment and install all dependencies
	@python3.8 -m pip install poetry==1.1.4
	@poetry install && \
	echo; echo "${CYAN}Created venv and installed all dependencies${COFF}"

shell: check-dotenv check-venv ## Run django-extension's shell_plus
	@./manage.py shell_plus --ipython

runserver: check-dotenv check-venv  ## Run dev server on port 8000, or specify with "make dev port=1234"
	@. ../.envs/local.env && if [ "$(DEBUG)" = 0 ]; then ./manage.py collectstatic --noinput --clear; fi
	@./manage.py migrate --noinput
	@./manage.py runserver $(port)
	@echo "${CYAN}Backend is running on localhost:$(port)${COFF}"

development: ## run dev docker
	@# Force recreate to reload NGINX config
	@# as it won't rebuild because the config is passed as a volume
	@docker-compose -f ${COMPOSE} up -d --build --force-recreate
	@echo "${CYAN}Backend is running on http://localhost:8880${COFF}"

stop: ## stop docker containers
	@docker-compose -f ${COMPOSE} down

clear: ## down containers and clear volumes
	@docker-compose -f ${COMPOSE} down --volumes

###############
# Code checks #
###############

check: check-venv ## Run linters
	@echo "flake8"
	@echo "======"
	@flake8 || exit 1
	@echo "OK"
	@echo;
	@echo "black"
	@echo "======"
	@black --check . || exit 1
	@echo;
	@echo "isort"
	@echo "======"
	@isort --check-only .

fix: check-venv ## Run code formatters
	@echo "autoflake"
	@echo "========="
	@# regex to exctrat per-file-ignores from .flake8
	@extract_ignores=$(shell echo "$$(grep ':F401' .flake8 | sed 's/:F401//' | sed -E 's/\W+//' | sed -E 'N;s/\n/,/' | sed -r 's/\x1B\[(;?[0-9]{1,3})+[mGK]//g')")
	@autoflake -ri --remove-all-unused-imports --exclude $$extract_ignores .
	@echo "black"
	@echo "====="
	@black .
	@echo;
	@echo "isort"
	@echo "====="
	@isort .
