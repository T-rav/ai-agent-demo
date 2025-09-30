# AI Agent Demo - Makefile
# Convenient commands for managing the application

.PHONY: help ui api start stop build test clean install logs lint format

# Default target
help:
	@echo "AI Agent Demo - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make start        - Start all services (UI + API when available)"
	@echo "  make stop         - Stop all running services"
	@echo "  make ui           - Start only the UI development server"
	@echo "  make api          - Start only the API server (when implemented)"
	@echo ""
	@echo "Ingest System:"
	@echo "  cd ingest && make help   - Show ingest commands (run from ingest/ folder)"
	@echo ""
	@echo "Building:"
	@echo "  make build        - Build all services for production"
	@echo "  make install      - Install dependencies for all services"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-ui      - Run UI tests only"
	@echo "  make test-api     - Run API tests only (when implemented)"
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
	# @make test-api  # Uncomment when API is implemented

# Run UI tests
test-ui:
	@echo "🧪 Running UI tests in Docker..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm test -- --coverage --watchAll=false

# Run ingest tests
test-ingest:
	@echo "🧪 Running ingest tests..."
	@cd ingest && make test

# UI-specific linting and formatting
lint-ui:
	@echo "🔍 Running UI linting in Docker..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run lint

format-check-ui:
	@echo "🔍 Checking UI formatting in Docker..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format:check

# Check TypeScript compilation
check:
	@echo "🔍 Checking TypeScript compilation in Docker..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npx tsc --noEmit

# Run API tests (placeholder)
test-api:
	@echo "🔧 API tests not yet implemented"
	# @docker-compose -f docker-compose.dev.yml run --rm api-dev pytest

# Lint all code
lint:
	@echo "🔍 Running linters in Docker..."
	@echo "Linting UI..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run lint
	@echo "✅ Linting complete"

# Lint and fix issues
lint-fix:
	@echo "🔧 Running linters with auto-fix in Docker..."
	@echo "Linting UI..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run lint:fix
	@echo "✅ Linting and fixes complete"

# Format code
format:
	@echo "✨ Formatting code in Docker..."
	@echo "Formatting UI..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format
	@echo "✅ Formatting complete"

# Check code formatting
format-check:
	@echo "🔍 Checking code formatting in Docker..."
	@echo "Checking UI formatting..."
	@docker-compose -f docker-compose.dev.yml run --rm frontend-dev npm run format:check
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

# For ingest commands, use: cd ingest && make <command>


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
ci: lint test
