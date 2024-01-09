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

check-python-version:
	@echo "Checking Python version..."
	@(python --version 2>&1 | grep "Python ${MIN_PYTHON_VERSION}" ) || (python3 --version 2>&1 | grep -q "Python 12" ) || \
	(echo -e "${RED}Error: Python 12 is not installed" && exit 1)

check-docker-version:
	@echo "Checking Docker version..."
	@(docker --version 2>&1 | grep -q "Docker version 2") || \
	(echo -e "${RED}Error: Docker version 2 is not installed." && exit 1)

##@ Environment
# Setup development environment for the first time
setup-environment: check-python-version check-docker-version
	@echo "Setting up the environment..."
	@bash -c "python -m venv .venv"
	@bash -c "source .venv/bin/activate && pip install --upgrade pip > /dev/null 2>&1 && pip install . > /dev/null 2>&1 && pre-commit install > /dev/null 2>&1"
	@echo -e "${GREEN}Environment is ready. Now run 'source .venv/bin/activate' from the commandline to activate the environment${NC}"

##@ Docker
# Start Docker containers
up:
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
