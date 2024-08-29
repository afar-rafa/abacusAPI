# Makefile for a Django project

# Variables
PYTHON = python3
MANAGE = $(PYTHON) manage.py
DJANGO_SETTINGS = config.settings.local

# Targets

.PHONY: help

help:
	@echo "Available commands:"
	@echo "  make migrate         - Run database migrations"
	@echo "  make runserver       - Start the Django development server"
	@echo "  make test            - Run Django tests"
	@echo "  make createsuperuser - Create a Django superuser"
	@echo "  make shell           - Open Django shell"

migrate:
	$(MANAGE) migrate

runserver:
	$(MANAGE) runserver

test:
	$(MANAGE) test

createsuperuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell
