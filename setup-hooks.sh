#!/bin/bash
# Setup pre-commit hooks for the project

set -e

echo "🔧 Setting up pre-commit hooks..."

# Function to install pre-commit
install_precommit() {
    # Check if we're in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo "📦 Installing pre-commit in virtual environment..."
        python -m pip install pre-commit
    # Check if project has a venv directory
    elif [[ -d "venv" ]]; then
        echo "📦 Found venv directory, installing pre-commit there..."
        source venv/bin/activate
        python -m pip install pre-commit
    # Try using --user flag for system-wide install
    else
        echo "📦 Installing pre-commit with --user flag..."
        python3 -m pip install --user pre-commit
        # Add user bin to PATH if not already there
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            export PATH="$HOME/.local/bin:$PATH"
            echo "   Added ~/.local/bin to PATH for this session"
        fi
    fi
}

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    install_precommit
else
    echo "✓ pre-commit already installed"
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
