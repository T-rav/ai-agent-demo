# AI Agent Demo - Makefile
# Convenient commands for managing the application

.PHONY: help ui api start stop build test clean install logs lint format

# Default target
help:
	@echo "AI Agent Demo - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make start        - Start all services (UI + API)"
	@echo "  make stop         - Stop all running services"
	@echo "  make ui           - Start only the UI development server"
	@echo "  make api          - Start only the API server"
	@echo "  make dev          - Alias for 'make start'"
	@echo ""
	@echo "Ingest System:"
	@echo "  make ingest       - Run document ingestion"
	@echo "  cd ingest && make help   - Show all ingest commands"
	@echo ""
	@echo "Building:"
	@echo "  make build        - Build all services for production"
	@echo "  make install      - Install dependencies for all services"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests (UI + API + Ingest)"
	@echo "  make test-ui      - Run UI tests only"
	@echo "  make test-api     - Run API tests only"
	@echo "  make test-ingest  - Run ingest tests only"
	@echo "  make check        - Check TypeScript compilation"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run linters on all code"
	@echo "  make lint-fix     - Run linters and fix issues automatically"
	@echo "  make format       - Format code with Prettier and Black"
	@echo "  make format-check - Check code formatting"
	@echo ""
	@echo "Utilities:"
	@echo "  make logs         - Show logs from running services"
	@echo "  make clean        - Clean build artifacts and dependencies"
	@echo "  make status       - Show status of running services"
	@echo "  make restart      - Restart all services"

# Start all services
start:
	@echo "🚀 Starting AI Agent Demo..."
	@if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then \
		echo "Starting services with Docker Compose..."; \
		docker-compose -f docker-compose.dev.yml up -d; \
	else \
		echo "Docker not available, starting UI in development mode..."; \
		make ui; \
	fi

# Stop all services
stop:
	@echo "🛑 Stopping AI Agent Demo..."
	@if docker-compose -f docker-compose.dev.yml ps -q 2>/dev/null | grep -q .; then \
		echo "Stopping Docker services..."; \
		docker-compose -f docker-compose.dev.yml down; \
	fi
	@echo "Stopping any remaining processes..."
	@pkill -f "react-scripts start" 2>/dev/null || true
	@pkill -f "npm start" 2>/dev/null || true
	@echo "✅ All services stopped"

# Start UI only
ui:
	@echo "🎨 Starting UI development server with Docker..."
	@docker-compose -f docker-compose.dev.yml up frontend-dev

# Start API only
api:
	@echo "🔧 Starting API server with Docker..."
	@docker-compose -f docker-compose.dev.yml up api-dev

# Build for production
build:
	@echo "🏗️  Building for production with Docker..."
	@docker-compose -f docker-compose.yml build
	@echo "✅ Build complete"

# Install dependencies (inside containers)
install:
	@echo "📦 Installing dependencies via Docker..."
	@echo "Building development containers will install dependencies..."
	@docker-compose -f docker-compose.dev.yml build
	@echo "✅ Dependencies installed"

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@make test-ui
	@make test-api
	@make test-ingest

# Run UI tests
test-ui:
	@if [ "$$CI" = "true" ]; then \
		echo "🧪 Running UI tests (CI mode)..."; \
		cd ui && npm test -- --coverage --watchAll=false; \
	else \
		echo "🧪 Running UI tests in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm test -- --coverage --watchAll=false; \
	fi

# Run ingest tests
test-ingest:
	@echo "🧪 Running ingest tests..."
	@cd ingest && make test

# UI-specific linting and formatting (Docker version for local dev)
lint-ui:
	@if [ "$$CI" = "true" ]; then \
		echo "🔍 Running UI linting (CI mode)..."; \
		cd ui && npm run lint; \
	else \
		echo "🔍 Running UI linting in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run lint; \
	fi

format-check-ui:
	@if [ "$$CI" = "true" ]; then \
		echo "🔍 Checking UI formatting (CI mode)..."; \
		cd ui && npm run format:check; \
	else \
		echo "🔍 Checking UI formatting in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format:check; \
	fi

# Check TypeScript compilation
check:
	@if [ "$$CI" = "true" ]; then \
		echo "🔍 Checking TypeScript compilation (CI mode)..."; \
		cd ui && npx tsc --noEmit; \
	else \
		echo "🔍 Checking TypeScript compilation in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npx tsc --noEmit; \
	fi

# Run API tests
test-api:
	@echo "🧪 Running API tests..."
	@if [ "$$CI" = "true" ]; then \
		echo "🧪 Running API tests (CI mode)..."; \
		cd api && python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=70 --cache-clear; \
	else \
		echo "🧪 Running API tests in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm api-dev pytest tests/ -v --cov=. --cov-report=term-missing --cov-fail-under=70 --cache-clear; \
	fi

# Lint all code
lint:
	@echo "🔍 Running linters on all services..."
	@make lint-ui
	@make lint-api
	@echo "✅ Linting complete"

# Lint API code
lint-api:
	@if [ "$$CI" = "true" ]; then \
		echo "🔍 Running API linting (CI mode)..."; \
		cd api && python -m flake8 . --exclude=tests,htmlcov,venv,.venv; \
	else \
		echo "🔍 Running API linting in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm api-dev python -m flake8 . --exclude=tests,htmlcov,venv,.venv; \
	fi

# Lint and fix issues
lint-fix:
	@if [ "$$CI" = "true" ]; then \
		echo "🔧 Running linters with auto-fix (CI mode)..."; \
		echo "Linting UI..."; \
		cd ui && npm run lint:fix; \
	else \
		echo "🔧 Running linters with auto-fix in Docker..."; \
		echo "Linting UI..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run lint:fix; \
	fi
	@echo "✅ Linting and fixes complete"

# Format code
format:
	@echo "✨ Formatting all services..."
	@make format-ui
	@make format-api
	@echo "✅ Formatting complete"

# Format UI code
format-ui:
	@if [ "$$CI" = "true" ]; then \
		echo "✨ Formatting UI (CI mode)..."; \
		cd ui && npm run format; \
	else \
		echo "✨ Formatting UI in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format; \
	fi

# Format API code
format-api:
	@if [ "$$CI" = "true" ]; then \
		echo "✨ Formatting API (CI mode)..."; \
		cd api && python -m black . && python -m isort .; \
	else \
		echo "✨ Formatting API in Docker..."; \
		docker-compose -f docker-compose.dev.yml run --rm api-dev bash -c "black . && isort ."; \
	fi

# Check code formatting
format-check:
	@if [ "$$CI" = "true" ]; then \
		echo "🔍 Checking code formatting (CI mode)..."; \
		echo "Checking UI formatting..."; \
		cd ui && npm run format:check; \
	else \
		echo "🔍 Checking code formatting in Docker..."; \
		echo "Checking UI formatting..."; \
		docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format:check; \
	fi
	@echo "✅ Format check complete"

# Show logs
logs:
	@echo "📋 Showing service logs..."
	@if docker-compose -f docker-compose.dev.yml ps -q 2>/dev/null | grep -q .; then \
		docker-compose -f docker-compose.dev.yml logs -f; \
	else \
		echo "No Docker services running. Check individual service logs."; \
	fi

# Clean build artifacts and dependencies
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf ui/build
	@rm -rf ui/node_modules
	@rm -rf ui/.npm
	@echo "Cleaning Docker resources..."
	@docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker system prune -f 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Show status of services
status:
	@echo "📊 Service Status:"
	@echo ""
	@echo "UI (Port 3000):"
	@if lsof -ti:3000 >/dev/null 2>&1; then \
		echo "  ✅ Running (PID: $$(lsof -ti:3000))"; \
	else \
		echo "  ❌ Not running"; \
	fi
	@echo ""
	@echo "API (Port 8000):"
	@if lsof -ti:8000 >/dev/null 2>&1; then \
		echo "  ✅ Running (PID: $$(lsof -ti:8000))"; \
	else \
		echo "  ❌ Not running"; \
	fi

# Ingest commands
ingest:
	@echo "🚀 Running document ingestion..."
	@cd ingest && make run

ingest-clean:
	@echo "🧹 Cleaning vector index..."
	@cd ingest && make run-clean

ingest-fresh:
	@echo "🚀 Running fresh ingestion (clean + ingest)..."
	@cd ingest && make run-fresh


# Clean all build artifacts
clean-all:
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf ui/build
	@rm -rf ui/node_modules
	@rm -rf ui/.npm
	@echo "Cleaning Docker resources..."
	@docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker-compose -f docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker system prune -f 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Install all dependencies
install-all:
	@echo "📦 Installing dependencies via Docker..."
	@echo "Building development containers will install dependencies..."
	@docker-compose -f docker-compose.dev.yml build
	@echo "✅ Dependencies installed"

# Development shortcuts
dev: start
prod: build
restart: stop start
ci:
	@echo "🔍 Running CI checks for all services..."
	@make format-check-ui
	@make lint-ui
	@make test-ui
	@make lint-api
	@make test-api
	@echo "✅ CI checks passed"
