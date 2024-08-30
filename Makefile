# Makefile for a Django project

# Variables
PYTHON = python3
MANAGE = $(PYTHON) manage.py
DJANGO_SETTINGS = config.settings.local

# Targets

.PHONY: help

help:
	@echo "Available commands:"
	@echo "  make migrations      - Write database migrations"
	@echo "  make migrate         - Run database migrations"
	@echo "  make run		      - Start the Django development server"
	@echo "  make test            - Run Django tests"
	@echo "  make superuser		  - Create a Django superuser"
	@echo "  make shell           - Open Django shell"

quick-setup:
	@echo "/*************************************************/"
	@echo "\t\tRunning Migrations"
	@echo "/*************************************************/"
	make migrate
	@echo "/*************************************************/"
	@echo "\t\tCreate Your User!"
	@echo "/*************************************************/"
	make superuser

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

run:
	$(MANAGE) runserver

test:
	$(MANAGE) test

superuser:
	$(MANAGE) createsuperuser

docker-build:
	docker compose build web --force-rm
docker-start:
	docker compose up --remove-orphans web
docker-shell:
	docker compose exec web bash
docker-down:
	docker compose down --remove-orphans
