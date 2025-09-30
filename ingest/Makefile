# AI Agent Demo - Ingest Makefile
# Commands for managing the document ingestion system

.PHONY: help install test lint format type-check security clean dev-install run-ingest query setup-db

# Default target
help:
	@echo "AI Agent Demo - Ingest System Commands:"
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
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-unit    - Run unit tests only"
	@echo "  make test-fast    - Run tests without coverage"
	@echo "  make test-verbose - Run tests with verbose output"
	@echo "  make coverage     - Generate coverage report"
	@echo ""
	@echo "Operations:"
	@echo "  make setup-db     - Setup Pinecone database"
	@echo "  make run-ingest   - Run document ingestion"
	@echo "  make query        - Run interactive query tool"
	@echo ""
	@echo "Development:"
	@echo "  make fix          - Auto-fix formatting and import issues"
	@echo "  make pre-commit   - Run all pre-commit checks"

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
	python -m flake8 .
	@echo "Running bandit security check..."
	python -m bandit -r . --severity-level medium
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
	python -m mypy .
	@echo "✅ Type checking complete"

security:
	@echo "🔒 Running security analysis..."
	python -m bandit -r . -f json -o bandit-report.json || true
	python -m bandit -r . --severity-level medium
	@echo "✅ Security analysis complete"

check-all: lint format-check type-check security
	@echo "✅ All code quality checks passed"

# Testing targets
test:
	@echo "🧪 Running tests with coverage..."
	python -m pytest tests/ -v --cov=ingest --cov-report=term-missing --cov-report=html

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
	python -m pytest tests/ --cov=ingest --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/"

# Operational targets
setup-db:
	@echo "🗄️  Setting up Pinecone database..."
	python -m ingest.core.setup

run-ingest:
	@echo "📥 Running document ingestion..."
	python -m ingest.core.ingest

query:
	@echo "🔍 Starting interactive query tool..."
	python -m ingest.core.query_test

# Development helpers
fix: format
	@echo "🔧 Auto-fixing code issues..."

pre-commit: format-check lint type-check test-fast
	@echo "✅ Pre-commit checks passed"

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
dev: dev-install
ci: check-all test
build: clean install
