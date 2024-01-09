# Makefile for managing a FastAPI application with Alembic and Docker

# Variables
MIN_PYTHON_VERSION = 3.12

DOCKER_COMPOSE = docker compose
COMPOSE_FILE = -f docker-compose.yml
ALEMBIC = alembic -c /backend/app/alembic.ini
RUFF = ruff
MAKEFLAGS += --no-print-directory
SHELL := /bin/bash

GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m # No Color


# Help
# Show this help.
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk '/^# / { help_message = substr($$0, 3); next } /^[a-zA-Z_-]+:/ { if (help_message) print "  \033[36m" $$1 "\033[0m" help_message; help_message = "" }' $(MAKEFILE_LIST)

##@ Docker
# Start Docker containers
up:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) build
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up --remove-orphans

# Stop Docker containers
down:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) down --remove-orphans

##@ FastAPI
# Run backend application
run-backend:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up backend

# Run database service
run-db:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up db -d

# Reset database service deleting all data
reset-db:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) stop db
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) rm -f db
	make run-db

##@ Alembic
# Show current Alembic revision
alembic-current:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) run backend $(ALEMBIC) current


# Upgrade to the latest Alembic revision
alembic-upgrade:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) run --rm backend $(ALEMBIC) upgrade head

# Downgrade to the previous Alembic revision
alembic-downgrade:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) run --rm backend $(ALEMBIC) downgrade -1

##@ Alembic
# Create a new Alembic revision
alembic-revision:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) run --rm backend $(ALEMBIC) revision --autogenerate -m "$(m)"

# Create a new Alembic revision with a message
migrate:
	make alembic-revision m="enter_migration_message_here"

##@ Testing
# Run tests with pytest
test: run-db
	pytest .

##@ Linting
# Lint code with Ruff
lint:
	$(RUFF) --fix .

# Phony targets
.PHONY: help up down run-backend run-db reset-db alembic-current alembic-upgrade alembic-downgrade alembic-revision migrate test lint

# Set the default goal to 'help' when no target is given
.DEFAULT_GOAL := help

# check-python-version
check-python-version:
	@echo "Checking Python ${MIN_PYTHON_VERSION}..."
	@(python --version 2>&1 | grep -q "Python ${MIN_PYTHON_VERSION}" ) || (python3 --version 2>&1 | grep -q "Python 12" ) || \
	(echo -e "${RED}Error: Python 12 is not installed" && exit 1)

check-docker-version:
	@echo "Checking if Docker 2 is installed..."
	@(docker compose version 2>&1) || \
	(echo -e "${RED}Error: Docker version 2 is not installed." && exit 1)

check-poetry:
	@echo "Checking if Poetry is installed..."
	@command -v poetry >/dev/null 2>&1 || { echo "Installing Poetry..."; curl -sSL https://install.python-poetry.org | python3 -; }

##@ Environment
# Setup development environment for the first time
setup-environment: check-docker-version check-python-version check-poetry
	@echo "Setting up the environment..."
	@bash -c "poetry env use python3.12 && poetry install"
	@echo -e "${GREEN}Environment is ready. Now run 'poetry shell' from the commandline to activate the environment${NC}"
