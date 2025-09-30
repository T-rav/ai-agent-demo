#!/usr / bin / env python3
"""
Setup script for the ingestion system.
Validates environment and dependencies.
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        return False
    print("✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies: {e}")
        return False


def check_environment_variables():
    """Check if required environment variables are set."""
    required_vars = ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]

    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)

    if missing_vars:
        print("⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   Please set these environment variables:")
        for var in missing_vars:
            print("     export {var}=your_value_here")
        print("   Or add them to your shell profile (.bashrc, .zshrc, etc.)")
        return False

    print("✅ Environment variables are set")
    return True


def check_pyproject_toml():
    """Check if pyproject.toml exists and has required configuration."""
    pyproject_file = Path("pyproject.toml")

    if not pyproject_file.exists():
        print("❌ pyproject.toml file not found")
        print("   This file should contain the project configuration")
        return False

    try:
        from config_loader import Config

        Config()
        print("✅ pyproject.toml configuration looks good")
        return True
    except Exception:
        print("❌ Error reading pyproject.toml: {e}")
        return False


def check_corpus_directory():
    """Check if corpus directory exists."""
    corpus_path = Path("../data / corpus")

    if not corpus_path.exists():
        print("❌ Corpus directory not found: {corpus_path.resolve()}")
        print("   Please ensure the data / corpus directory exists with documents")
        return False

    # Count documents
    supported_extensions = {".pdf", ".md", ".txt"}
    doc_count = 0

    for root, dirs, files in os.walk(corpus_path):
        for file in files:
            if Path(file).suffix.lower() in supported_extensions:
                doc_count += 1

    if doc_count == 0:
        print("⚠️  No supported documents found in {corpus_path.resolve()}")
        print("   Supported formats: PDF, Markdown (.md), Text (.txt)")
        return False

    print("✅ Found {doc_count} documents in corpus directory")
    return True


def test_api_connections():
    """Test API connections."""
    print("🔗 Testing API connections...")

    # Test OpenAI
    try:
        from openai import OpenAI

        client = OpenAI()

        # Test with a simple embedding request
        response = client.embeddings.create(model="text - embedding - 3-small", input="test")
        print("✅ OpenAI API connection successful")
    except Exception:
        print("❌ OpenAI API test failed: {str(e)}")
        return False

    # Test Pinecone
    try:
        from pinecone import Pinecone

        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

        # List indexes to test connection
        pc.list_indexes()
        print("✅ Pinecone API connection successful")
    except Exception:
        print("❌ Pinecone API test failed: {str(e)}")
        return False

    return True


def main():
    """Run setup validation."""
    print("🚀 AI Agent Demo - Ingestion Setup")
    print("=" * 40)

    checks = [
        ("Python Version", check_python_version),
        ("pyproject.toml", check_pyproject_toml),
        ("Dependencies", install_dependencies),
        ("Environment Variables", check_environment_variables),
        ("Corpus Directory", check_corpus_directory),
        ("API Connections", test_api_connections),
    ]

    all_passed = True

    for check_name, check_func in checks:
        print("\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False

    print("\n" + "=" * 40)

    if all_passed:
        print("🎉 Setup validation passed!")
        print("\nYou can now run the ingestion:")
        print("   python ingest.py")
        print("   # or use the installed command:")
        print("   ingest - corpus")
        print("\nOr test queries:")
        print("   python query_test.py --interactive")
        print("   # or use the installed command:")
        print("   query - corpus --interactive")
    else:
        print("❌ Setup validation failed!")
        print("Please fix the issues above before running ingestion.")
        sys.exit(1)


if __name__ == "__main__":
    main()
