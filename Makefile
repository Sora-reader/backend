##########
# Config #
##########

COMPOSE=docker-compose.yml
port?=8000

.PHONY: help env venv shell dev \
 		check fix

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###########
# Project #
###########

interpreter := $(shell [ -d "$$(poetry env info --path)" ] && echo "poetry run")

check-dotenv:
	@$(eval DOTENVS := $(shell test -f ./.envs/docker.env && test -f ./.envs/local.env && echo 'nonzero string'))
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
	@echo "Done"


venv: ## Create virtual environment and install all dependencies
	@python3.8 -m pip install poetry==1.1.4
	@poetry install && \
	echo; echo "Created venv and installed all dependencies"

shell: check-dotenv check-venv ## Run django-extension's shell_plus
	@$(interpreter) ./manage.py shell_plus --ipython

runserver: check-dotenv check-venv  ## Run dev server on port 8000, or specify with "make dev port=1234"
	@. ../.envs/local.env && if [ "$(DEBUG)" = 0 ]; then $(interpreter) ./manage.py collectstatic --noinput --clear; fi
	@$(interpreter) ./manage.py migrate --noinput
	@$(interpreter) ./manage.py runserver $(port)
	@echo "Backend is running on localhost:$(port)"

development: ## run dev docker
	@# Force recreate to reload NGINX config
	@# as it won't rebuild because the config is passed as a volume
	@docker-compose -f ${COMPOSE} up -d --build --force-recreate
	@echo "Backend is running on localhost:8880"

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
	@echo "autoflake"
	@echo "========="
	@extract_ignores=$(shell echo "$$(grep ':F401' .flake8 | sed 's/:F401//' | sed -E 's/\W+//' | sed -E 'N;s/\n/,/' | sed -r 's/\x1B\[(;?[0-9]{1,3})+[mGK]//g')")
	@$(interpreter) autoflake -ri --remove-all-unused-imports --exclude $$extract_ignores .
	@echo "black"
	@echo "====="
	@$(interpreter) black .
	@echo;
	@echo "isort"
	@echo "====="
	@$(interpreter) isort .
