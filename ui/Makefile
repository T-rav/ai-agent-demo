# AI Agent Demo - UI Makefile
# Commands for managing the React frontend

.PHONY: help install test lint format type-check security clean dev build start preview coverage check-all

# Default target
help:
	@echo "AI Agent Demo - UI Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      - Install production dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make clean        - Clean build artifacts and cache"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         - Run ESLint"
	@echo "  make lint-fix     - Run ESLint and fix issues"
	@echo "  make format       - Format code with Prettier"
	@echo "  make format-check - Check code formatting without changes"
	@echo "  make type-check   - Run TypeScript type checking"
	@echo "  make check-all    - Run all code quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests with coverage"
	@echo "  make test-watch   - Run tests in watch mode"
	@echo "  make test-fast    - Run tests without coverage"
	@echo "  make coverage     - Generate coverage report"
	@echo ""
	@echo "Operations:"
	@echo "  make dev          - Run development server"
	@echo "  make start        - Alias for 'make dev'"
	@echo "  make build        - Build for production"
	@echo "  make preview      - Preview production build"
	@echo ""
	@echo "Development:"
	@echo "  make fix          - Auto-fix formatting and linting issues"
	@echo "  make pre-commit   - Run all pre-commit checks"
	@echo "  make ci           - Run CI checks (format-check, lint, type-check, test)"

# Installation targets
install:
	@echo "📦 Installing production dependencies..."
	npm ci --production

dev-install:
	@echo "📦 Installing development dependencies..."
	npm ci
	@echo "✅ Dependencies installed"

# Code quality targets
lint:
	@echo "🔍 Running ESLint..."
	npm run lint
	@echo "✅ Linting complete"

lint-fix:
	@echo "🔧 Running ESLint with auto-fix..."
	npm run lint:fix
	@echo "✅ Linting and fixes complete"

format:
	@echo "✨ Formatting code with Prettier..."
	npm run format
	@echo "✅ Formatting complete"

format-check:
	@echo "🔍 Checking code formatting..."
	npm run format:check
	@echo "✅ Format check complete"

type-check:
	@echo "🔍 Running TypeScript type checking..."
	npx tsc --noEmit
	@echo "✅ Type checking complete"

check-all: format-check lint type-check
	@echo "✅ All code quality checks passed"

# Testing targets
test:
	@echo "🧪 Running tests with coverage..."
	npm test -- --coverage --watchAll=false

test-watch:
	@echo "🧪 Running tests in watch mode..."
	npm test

test-fast:
	@echo "🧪 Running fast tests..."
	npm test -- --watchAll=false

coverage:
	@echo "📊 Generating coverage report..."
	npm test -- --coverage --watchAll=false
	@echo "Coverage report generated in coverage/"
	@echo "Open coverage/lcov-report/index.html to view detailed report"

# Operational targets
dev:
	@echo "🚀 Starting development server..."
	npm start

start: dev

build:
	@echo "🏗️  Building for production..."
	npm run build
	@echo "✅ Build complete (output in build/)"

preview:
	@echo "🔍 Previewing production build..."
	@echo "Note: You need to serve the build/ directory with a static server"
	@which serve > /dev/null && npx serve -s build -p 3000 || echo "Install 'serve' with: npm install -g serve"

# Development helpers
fix: format lint-fix
	@echo "🔧 Auto-fixing code issues..."
	@echo "✅ All fixes applied"

pre-commit: format-check lint type-check test-fast
	@echo "✅ Pre-commit checks passed"

ci: format-check lint type-check test
	@echo "✅ CI checks passed"

# Cleanup
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf coverage/
	rm -rf node_modules/.cache/
	rm -rf .npm/
	@echo "✅ Cleanup complete"

clean-all: clean
	@echo "🧹 Cleaning all dependencies..."
	rm -rf node_modules/
	@echo "✅ Full cleanup complete"

# Shortcuts
c: clean
b: build
d: dev
t: test
l: lint
f: format

