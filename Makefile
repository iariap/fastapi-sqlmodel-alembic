# Makefile for managing a FastAPI application with Alembic and Docker

# Variables
DOCKER_COMPOSE = docker compose
COMPOSE_FILE = -f docker-compose.yml
ALEMBIC = alembic -c /app/alembic.ini
RUFF = ruff
MAKEFLAGS += --no-print-directory


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
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up -d

# Stop Docker containers
down:
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) down

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
	@read -p "Enter revision message: " REVISION_MESSAGE; \
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) run --rm backend $(ALEMBIC) revision --autogenerate -m "$$REVISION_MESSAGE"


# Create a new Alembic revision with a message
migrate:
	make alembic-revision m="enter_migration_message_here"

##@ Testing
# Run tests with pytest
test:
	pytest app/tests

##@ Linting
# Lint code with Ruff
lint:
	$(RUFF) app/

# Phony targets
.PHONY: help up down run-backend run-db reset-db alembic-current alembic-upgrade alembic-downgrade alembic-revision migrate test lint

# Set the default goal to 'help' when no target is given
.DEFAULT_GOAL := help
