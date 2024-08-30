# Makefile for a Django project

# Variables
PYTHON = python3
MANAGE = $(PYTHON) manage.py

# Targets

.PHONY: help

help:
	@echo "Available commands:"
	@echo "  make migrations      - Write database migrations"
	@echo "  make migrate         - Run database migrations"
	@echo "  make test		      - Run format tests"
	@echo "  make format          - Run formatters"
	@echo "  make superuser		  - Create a Django superuser"

	@echo "Docker commands:"
	@echo "  make docker-build    - Build the docker image"
	@echo "  make docker-start    - Start the API container"
	@echo "  make docker-shell    - Exec into the container"
	@echo "  make quick-setup     - Setup the Database"
	@echo "  make docker-down     - Shutdown the service"

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

test:
	black --check .
	isort --check .

format:
	black .
	isort .

superuser:
	$(MANAGE) createsuperuser

docker-build:
	docker compose -f docker/docker-compose.yml build web --force-rm
docker-start:
	docker compose -f docker/docker-compose.yml up --remove-orphans web
docker-shell:
	docker compose -f docker/docker-compose.yml exec web bash

quick-setup:
	@echo "/*************************************************/"
	@echo "\t\tRunning Migrations"
	@echo "/*************************************************/"
	make migrate
	@echo "/*************************************************/"
	@echo "\t\tCreate Your User!"
	@echo "/*************************************************/"
	make superuser

docker-stop:
	docker compose -f docker/docker-compose.yml down --remove-orphans
