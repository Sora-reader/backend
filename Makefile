##########
# Config #
##########

.PHONY: help env venv githooks shell run \
 		test check fix \
		run stop test-ignore show-build-files \
		check-venv

.ONESHELL:

.DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###########
# Project #
###########

check-venv: ## Check that the virtual env is active and error if not.
ifndef VIRTUAL_ENV
	$(error Not in a virtual environment. Activate your venv and try again)
endif

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
	@python3.8 -m venv venv || exit 1
	@. venv/bin/activate && poetry install && \
	echo; echo "activate virtual environment with \". venv/bin/activate\""

githooks: ## Install git hooks
	@cd .git/hooks
	@ln -sf ../../githooks/pre-commit . && \
	echo "Installed git hooks"

shell: check-venv ## Run django-extension's shell_plus
	@./manage.py shell_plus --ipython

dev: check-venv ## Run dev server on port 8000, or specify with "make dev port=1234"
	@. .envs/local.env && if [ "$$DEBUG" = 0 ]; then python manage.py collectstatic --noinput --clear; fi
	@. .envs/local.env && python manage.py migrate --noinput
	@./manage.py runserver $(port)

###############
# Code checks #
###############

test: check-venv ## Test code with pytest
	@echo "pytest"
	@echo "======"
	@poetry run pytest

check: check-venv ## Run linters
	@echo "flake8"
	@echo "======"
	@poetry run flake8 || exit 1
	@echo "OK"
	@echo;
	@echo "black"
	@echo "======"
	@poetry run black --check . || exit 1
	@echo;
	@echo "isort"
	@echo "======"
	@poetry run isort --check-only .

fix: check-venv ## Run code formatters
	@echo "black"
	@echo "====="
	@poetry run black .
	@echo;
	@echo "autoflake"
	@echo "========="
	@poetry run autoflake . --recursive --in-place --remove-all-unused-imports --remove-duplicate-keys \
				--exclude=__init__.py,build,dist,.git,.eggs,migrations,venv
	@echo;
	@echo "isort"
	@echo "====="
	@poetry run isort .

##########
# Docker #
##########

run: ## Run production containers
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
