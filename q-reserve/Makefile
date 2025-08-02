.PHONY: help install test lint format clean docker-build docker-run docker-stop seed migrate

help: ## Show this help message
	@echo "q-reserve - Helpdesk/Ticketing System"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=backend --cov-report=html --cov-report=term-missing

lint: ## Run linting
	black --check backend/
	isort --check-only backend/
	ruff check backend/

format: ## Format code
	black backend/
	isort backend/
	ruff check --fix backend/

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

docker-build: ## Build Docker image
	docker-compose build

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

seed: ## Seed database with initial data
	python scripts/seed_data.py

migrate: ## Run database migrations
	alembic upgrade head

migrate-create: ## Create new migration
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

dev: ## Start development server
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

celery: ## Start Celery worker
	celery -A backend.app.core.celery worker --loglevel=info

setup: install migrate seed ## Complete setup (install, migrate, seed)
	@echo "Setup complete! Run 'make dev' to start the development server." 