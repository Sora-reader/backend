##########
# Config #
##########

# TODO: check venv, remove hadrcoding venv/bin/activate

PYTHON = $(shell which python3 || which python)

.PHONY: help env venv githooks shell run \
 		test check fix \
 		run stop test-ignore show-build-files

.ONESHELL:
.DEFAULT: help
help:
	@echo "Project"
	@echo "======="
	@echo "make env"
	@echo "	   copy env examples and init .envs directory"
	@echo "make venv"
	@echo "	   create virtual environment and install all dependencies"
	@echo "make githooks"
	@echo "	   install git hooks"
	@echo "make shell"
	@echo "	   run django-extension's shell_plus"
	@echo "make dev (make dev port=1234)"
	@echo "	   run dev server any port or 8000"
	@echo;
	@echo "Code checks"
	@echo "==========="
	@echo "make test"
	@echo "	   test code with pytest"
	@echo "make check"
	@echo "	   run linters"
	@echo "make fix"
	@echo "	   run code formatters"
	@echo;
	@echo "Docker"
	@echo "======"
	@echo "make run / make stop"
	@echo "	   run or stop production containers"
	@echo "make test-ignore"
	@echo "	   test local .dockerignore, output local files after build"
	@echo "make show-build-files"
	@echo "	   build Dockerfile and output WORKDIR files"

###########
# Project #
###########

env:
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

venv:
	@$(PYTHON) -m pip install poetry==1.1.4
	@$(PYTHON) -m venv venv
	@. venv/bin/activate && poetry install

githooks:
	@cd .git/hooks; \
	ln -sf ../../githooks/pre-commit .;

shell:
	@. venv/bin/activate && ./manage.py shell_plus --ipython

dev:
	@. .envs/local.env && if [ "$$DEBUG" = 0 ]; then python manage.py collectstatic --noinput --clear; fi
	@. .envs/local.env && python manage.py migrate --noinput
	@. venv/bin/activate && ./manage.py runserver $(port)

###############
# Code checks #
###############

test:
	@echo "pytest"
	@echo "======"
	@poetry run pytest

check:
	@echo "flake8" && \
	echo "======" && \
	poetry run flake8 && \
	echo "OK" && echo "" && \
	echo "black" && \
	echo "======" && \
	poetry run black --check . && echo "" &&\
	echo "isort" && \
	echo "======" && \
	poetry run isort --check-only .

fix:
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

run:
	@docker-compose up -d --build
	@echo;
	@echo "Backend is running on http://localhost:5500, the db is available at localhost:5502"

stop:
	@docker-compose down

show-build-files:
	@docker build -t test-dockerfile .
	@docker run --rm --entrypoint=/bin/sh test-dockerfile -c find .

test-ignore:
	@cat <<EOF > Dockerfile.build-context
	@FROM busybox
	@COPY $(COMPOSE_DIR) /build-context
	@WORKDIR /build-context
	@CMD find .
	@EOF
	@docker build -f Dockerfile.build-context -t build-context .
	@docker run --rm -it build-context
	@rm Dockerfile.build-context
