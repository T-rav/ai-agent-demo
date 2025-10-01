"""
Pytest configuration and fixtures for the API tests.
Following ingest pattern: builders/factories are used directly in tests, not as fixtures.
"""

import pytest


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables for testing."""
    env_vars = {
        "OPENAI_API_KEY": "test-openai-key",
        "OPENAI_MODEL": "gpt-4-turbo-preview",
        "PINECONE_API_KEY": "test-pinecone-key",
        "PINECONE_ENVIRONMENT": "test-env",
        "PINECONE_INDEX_NAME": "test-index",
        "EMBEDDING_MODEL": "text-embedding-3-small",
        "EMBEDDING_DIMENSIONS": "1536",
        "RETRIEVAL_K": "5",
        "TAVILY_API_KEY": "test-tavily-key",
        "LANGCHAIN_TRACING_V2": "false",
        "LANGCHAIN_API_KEY": "",
        "LANGCHAIN_PROJECT": "test-project",
        "DEBUG": "true",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


# ============================================================================
# Common Test Data - Only for frequently reused data
# ============================================================================


@pytest.fixture
def sample_chat_request_dict():
    """Sample chat request as dictionary for API calls.
    This is a fixture because it's used in many endpoint tests.
    """
    return {
        "message": "What is RAG?",
        "conversation_history": [],
        "session_id": "test-session-123",
        "research_mode": False,
    }
