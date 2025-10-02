# AI Agent Demo - API Makefile
# Commands for managing the API service

.PHONY: help install test lint format type-check security clean dev-install run dev coverage check-all

# Default target
help:
	@echo "AI Agent Demo - API Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make clean        - Clean build artifacts and cache"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run all linters (flake8, bandit)"
	@echo "  make format       - Format code with black and isort"
	@echo "  make format-check - Check code formatting without changes"
	@echo "  make type-check   - Run mypy type checking"
	@echo "  make security     - Run security analysis with bandit"
	@echo "  make check-all    - Run all code quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests with coverage (requires 70%)"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-fast    - Run tests without coverage"
	@echo "  make test-verbose - Run tests with verbose output"
	@echo "  make coverage     - Generate coverage report"
	@echo ""
	@echo "Operations:"
	@echo "  make run          - Run API server in development mode"
	@echo "  make dev          - Run API server with hot reload"
	@echo ""
	@echo "Development:"
	@echo "  make fix          - Auto-fix formatting and import issues"
	@echo "  make pre-commit   - Run all pre-commit checks"
	@echo "  make ci           - Run CI checks (format-check, lint, test)"

# Installation targets
install:
	@echo "📦 Installing production dependencies..."
	pip install -e .

dev-install:
	@echo "📦 Installing development dependencies..."
	pip install -e ".[dev]"

# Code quality targets
lint:
	@echo "🔍 Running linters..."
	@echo "Running flake8..."
	python -m flake8 . --exclude=tests,htmlcov,venv,.venv
	@echo "Running bandit security check..."
	python -m bandit -r . --exclude ./tests,./htmlcov,./venv,./.venv -ll
	@echo "✅ Linting complete"

format:
	@echo "✨ Formatting code..."
	python -m black .
	python -m isort .
	@echo "✅ Formatting complete"

format-check:
	@echo "🔍 Checking code formatting..."
	python -m black --check --diff .
	python -m isort --check-only --diff .
	@echo "✅ Format check complete"

type-check:
	@echo "🔍 Running type checking..."
	python -m mypy . --exclude tests --exclude htmlcov
	@echo "✅ Type checking complete"

security:
	@echo "🔒 Running security analysis..."
	python -m bandit -r . -f json -o bandit-report.json --exclude ./tests,./htmlcov,./venv,./.venv || true
	python -m bandit -r . --exclude ./tests,./htmlcov,./venv,./.venv -ll
	@echo "✅ Security analysis complete"

check-all: format-check lint security
	@echo "✅ All code quality checks passed"

# Testing targets
test:
	@echo "🧪 Running tests with coverage (minimum 70%)..."
	python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=70

test-unit:
	@echo "🧪 Running unit tests..."
	python -m pytest tests/ -v -m "not integration"

test-fast:
	@echo "🧪 Running fast tests..."
	python -m pytest tests/ -v --no-cov

test-verbose:
	@echo "🧪 Running verbose tests..."
	python -m pytest tests/ -vv --tb=long

coverage:
	@echo "📊 Generating coverage report..."
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-fail-under=70
	@echo "Coverage report generated in htmlcov/"
	@echo "Open htmlcov/index.html to view detailed report"

# Operational targets
run:
	@echo "🚀 Starting API server..."
	uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	@echo "🚀 Starting API server with hot reload..."
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Development helpers
fix: format
	@echo "🔧 Auto-fixing code issues..."

pre-commit: format-check lint test-fast
	@echo "✅ Pre-commit checks passed"

ci: format-check lint test
	@echo "✅ CI checks passed"

# Cleanup
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f coverage.xml
	rm -f bandit-report.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

# Shortcuts
build: clean install
