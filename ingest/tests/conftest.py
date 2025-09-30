"""
Pytest configuration and fixtures for the ingestion system tests.
Enhanced with factories, builders, and shared test utilities.
"""

from pathlib import Path

import pytest

from ..models import FileType, ProcessedDocument
from .builders import (
    a_markdown_document,
    a_pdf_document,
    a_processed_document,
    a_text_document,
    an_ingestion_config,
)
from .factories import ConfigFactory, ContentFactory, TestDataSamples, TokenFactory
from .utils import MockContextManager, TestDataGenerator, TestScenarios


@pytest.fixture
def mock_token_encoder():
    """Mock token encoder for testing."""
    return TokenFactory.create_simple_mock_token_encoder()


@pytest.fixture
def sample_markdown_content():
    """Sample markdown content for testing."""
    return ContentFactory.create_sample_markdown_content()


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing."""
    return ContentFactory.create_sample_pdf_content()


@pytest.fixture
def sample_text_content():
    """Sample text content for testing."""
    return ContentFactory.create_sample_text_content()


@pytest.fixture
def sample_document(sample_markdown_content, mock_token_encoder):
    """Provide a sample processed document for testing."""
    return ProcessedDocument(
        file_name="sample.md",
        file_type=FileType.MARKDOWN,
        title="Introduction to AI",
        content=sample_markdown_content,
        token_count=mock_token_encoder.count_tokens(sample_markdown_content),
        char_count=len(sample_markdown_content),
    )


@pytest.fixture
def temp_test_file(tmp_path):
    """Create a temporary test file."""

    def _create_file(content: str, filename: str = "test.md") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content)
        return file_path

    return _create_file


# ============================================================================
# New Factory - Based Fixtures
# ============================================================================


@pytest.fixture
def mock_text_cleaner():
    """Mock text cleaner for testing."""
    return ContentFactory.create_mock_text_cleaner()


@pytest.fixture
def mock_config():
    """Mock configuration object for testing."""
    return ConfigFactory.create_mock_config()


# ============================================================================
# Document Builder Fixtures
# ============================================================================


@pytest.fixture
def markdown_document():
    """Markdown document for testing."""
    return a_markdown_document().build()


@pytest.fixture
def pdf_document():
    """PDF document for testing."""
    return a_pdf_document().build()


@pytest.fixture
def text_document():
    """Text document for testing."""
    return a_text_document().build()


@pytest.fixture
def large_document():
    """Large document for chunking tests."""
    return a_processed_document().with_long_content().build()


@pytest.fixture
def empty_document():
    """Empty document for edge case tests."""
    return a_processed_document().with_empty_content().build()


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def default_config():
    """Default ingestion configuration."""
    return an_ingestion_config().build()


@pytest.fixture
def production_config():
    """Production ingestion configuration."""
    return an_ingestion_config().for_production().build()


@pytest.fixture
def development_config():
    """Development ingestion configuration."""
    return an_ingestion_config().for_development().build()


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def basic_env_vars():
    """Basic environment variables for testing."""
    return TestDataSamples.BASIC_ENV_VARS.copy()


@pytest.fixture
def extended_env_vars():
    """Extended environment variables for testing."""
    return TestDataSamples.EXTENDED_ENV_VARS.copy()


@pytest.fixture
def empty_env_vars():
    """Empty environment variables for testing."""
    return TestDataSamples.EMPTY_ENV_VARS.copy()


@pytest.fixture
def sample_toml_config():
    """Sample TOML configuration content."""
    return TestDataSamples.SAMPLE_TOML_CONFIG


@pytest.fixture
def sample_env_content():
    """Sample .env file content."""
    return TestDataSamples.SAMPLE_ENV_CONTENT


# ============================================================================
# Scenario Fixtures
# ============================================================================


@pytest.fixture
def markdown_processing_scenario():
    """Complete markdown processing test scenario."""
    return TestScenarios.create_markdown_processing_scenario()


@pytest.fixture
def pdf_processing_scenario():
    """Complete PDF processing test scenario."""
    return TestScenarios.create_pdf_processing_scenario()


@pytest.fixture
def text_chunking_scenario():
    """Text chunking test scenario."""
    return TestScenarios.create_chunking_scenario("text")


# ============================================================================
# Mock Context Manager Fixtures
# ============================================================================


@pytest.fixture
def mock_file_ops():
    """Mock file operations context manager."""
    return MockContextManager.mock_file_operations


@pytest.fixture
def mock_config_loading():
    """Mock configuration loading context manager."""
    return MockContextManager.mock_config_loading


@pytest.fixture
def mock_env_vars():
    """Mock environment variables context manager."""
    return MockContextManager.mock_environment_variables


# ============================================================================
# Utility Fixtures
# ============================================================================


@pytest.fixture
def test_data_generator():
    """Test data generator utility."""
    return TestDataGenerator


@pytest.fixture
def test_scenarios():
    """Test scenarios utility."""
    return TestScenarios
