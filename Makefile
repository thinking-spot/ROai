.PHONY: help build up down logs clean test

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker containers"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make clean    - Remove containers and volumes"
	@echo "  make test     - Run tests"
	@echo "  make migrate  - Run database migrations"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

test:
	docker-compose exec backend pytest

migrate:
	docker-compose exec backend alembic upgrade head

shell:
	docker-compose exec backend /bin/bash

db-shell:
	docker-compose exec postgres psql -U roai_user -d roai_db
