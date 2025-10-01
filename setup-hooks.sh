#!/bin/bash
# Setup pre-commit hooks for the project

set -e

echo "🔧 Setting up pre-commit hooks..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
fi

# Install the git hooks
echo "🪝 Installing git hooks..."
pre-commit install

# Run on all files to check everything is working
echo "✅ Running pre-commit on all files..."
pre-commit run --all-files || echo "⚠️  Some files need formatting. They've been auto-fixed. Please review and commit."

echo ""
echo "✨ Pre-commit hooks installed successfully!"
echo "   Hooks will now run automatically before each commit."
echo ""
echo "💡 Tips:"
echo "   - To skip hooks: git commit --no-verify"
echo "   - To run manually: pre-commit run --all-files"
echo "   - To update hooks: pre-commit autoupdate"

