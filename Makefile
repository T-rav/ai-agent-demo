# AI Agent Demo - Makefile
# Convenient commands for managing the application

.PHONY: help ui api ingest start stop build test clean install logs lint format

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
	@echo "  make ingest-help  - Show ingest-specific commands"
	@echo "  make ingest-setup - Setup ingest system and database"
	@echo "  make ingest-run   - Run document ingestion"
	@echo "  make ingest-query - Interactive query tool"
	@echo "  make ingest-test  - Run ingest tests"
	@echo "  make ingest-lint  - Run ingest linting"
	@echo ""
	@echo "Building:"
	@echo "  make build        - Build all services for production"
	@echo "  make install      - Install dependencies for all services"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-ui      - Run UI tests only"
	@echo "  make test-ingest  - Run ingest tests only"
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
	@echo "🎨 Starting UI development server..."
	@if lsof -ti:3000 >/dev/null 2>&1; then \
		echo "⚠️  Port 3000 is already in use. Stopping existing process..."; \
		kill -9 $$(lsof -ti:3000) 2>/dev/null || true; \
		sleep 2; \
	fi
	@echo "Starting React development server..."
	@cd ui && npm start

# Start API only (placeholder for future implementation)
api:
	@echo "🔧 API server not yet implemented"
	@echo "This will start the Python FastAPI server when available"
	# @cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Build for production
build:
	@echo "🏗️  Building for production..."
	@echo "Building UI..."
	@cd ui && npm run build
	@echo "✅ Build complete"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@echo "Installing UI dependencies..."
	@cd ui && npm install
	@echo "✅ Dependencies installed"

# Run all tests
test:
	@echo "🧪 Running all tests..."
	@make test-ui
	@make test-ingest
	# @make test-api  # Uncomment when API is implemented

# Run UI tests
test-ui:
	@echo "🧪 Running UI tests..."
	@cd ui && npm test -- --coverage --watchAll=false

# Run ingest tests
test-ingest:
	@echo "🧪 Running ingest tests..."
	@cd ingest && make test

# Check TypeScript compilation
check:
	@echo "🔍 Checking TypeScript compilation..."
	@cd ui && npx tsc --noEmit

# Run API tests (placeholder)
test-api:
	@echo "🔧 API tests not yet implemented"
	# @cd backend && python -m pytest

# Lint all code
lint:
	@echo "🔍 Running linters..."
	@echo "Linting UI..."
	@cd ui && npm run lint
	@echo "Linting ingest..."
	@cd ingest && make lint
	@echo "✅ Linting complete"

# Lint and fix issues
lint-fix:
	@echo "🔧 Running linters with auto-fix..."
	@echo "Linting UI..."
	@cd ui && npm run lint:fix
	@echo "Fixing ingest formatting..."
	@cd ingest && make fix
	@echo "✅ Linting and fixes complete"

# Format code
format:
	@echo "✨ Formatting code..."
	@echo "Formatting UI..."
	@cd ui && npm run format
	@echo "Formatting ingest..."
	@cd ingest && make format
	@echo "✅ Formatting complete"

# Check code formatting
format-check:
	@echo "🔍 Checking code formatting..."
	@echo "Checking UI formatting..."
	@cd ui && npm run format:check
	@echo "Checking ingest formatting..."
	@cd ingest && make format-check
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

# Ingest-specific commands
ingest-help:
	@echo "📥 Ingest System Commands:"
	@cd ingest && make help

ingest-setup:
	@echo "🔧 Setting up ingest system..."
	@cd ingest && make dev-install && make setup-db

ingest-run:
	@echo "📥 Running document ingestion..."
	@cd ingest && make run-ingest

ingest-query:
	@echo "🔍 Starting interactive query tool..."
	@cd ingest && make query

ingest-test:
	@echo "🧪 Running ingest tests..."
	@cd ingest && make test

ingest-lint:
	@echo "🔍 Running ingest linting..."
	@cd ingest && make lint

ingest-clean:
	@echo "🧹 Cleaning ingest artifacts..."
	@cd ingest && make clean

# Install ingest dependencies
install-ingest:
	@echo "📦 Installing ingest dependencies..."
	@cd ingest && make dev-install

# Clean ingest artifacts
clean-ingest:
	@echo "🧹 Cleaning ingest build artifacts..."
	@cd ingest && make clean

# Update clean target to include ingest
clean: clean-ingest
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf ui/build
	@rm -rf ui/node_modules
	@rm -rf ui/.npm
	@echo "Cleaning Docker resources..."
	@docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans 2>/dev/null || true
	@docker system prune -f 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Update install target to include ingest
install: install-ingest
	@echo "📦 Installing dependencies..."
	@echo "Installing UI dependencies..."
	@cd ui && npm install
	@echo "Installing ingest dependencies..."
	@cd ingest && make dev-install
	@echo "✅ Dependencies installed"

# Development shortcuts
dev: start
prod: build
restart: stop start
ci: lint test
