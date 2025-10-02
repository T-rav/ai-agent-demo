"""
Tests for configuration module.
"""

import pytest
from pydantic import ValidationError


class TestSettingsConfiguration:
    """Tests for Settings configuration."""

    def test_settings_loads_from_env(self, mock_env_vars):
        """Test that settings load correctly from environment variables."""
        from config import Settings

        settings = Settings()
        assert settings.openai_api_key == "test-openai-key"
        assert settings.pinecone_api_key == "test-pinecone-key"
        assert settings.pinecone_index_name == "test-index"

    def test_settings_has_required_fields(self, mock_env_vars):
        """Test that settings has all required fields."""
        from config import Settings

        settings = Settings()
        assert hasattr(settings, "openai_api_key")
        assert hasattr(settings, "pinecone_api_key")
        assert hasattr(settings, "pinecone_environment")

    def test_settings_defaults(self, mock_env_vars):
        """Test that settings has correct defaults."""
        from config import Settings

        settings = Settings()
        assert settings.openai_model == "gpt-4-turbo-preview"
        assert settings.embedding_model == "text-embedding-3-small"
        assert settings.retrieval_k == 5

    def test_settings_optional_fields(self, mock_env_vars):
        """Test that optional fields work correctly."""
        from config import Settings

        settings = Settings()
        assert settings.tavily_api_key == "test-tavily-key"
        assert settings.langchain_project == "test-project"

    def test_settings_without_required_fields(self, monkeypatch):
        """Test that settings raises error without required fields."""
        from config import Settings

        # Clear required environment variables
        for key in ["OPENAI_API_KEY", "PINECONE_API_KEY", "PINECONE_ENVIRONMENT"]:
            monkeypatch.delenv(key, raising=False)

        # Clear the .env file path so it doesn't load from file
        monkeypatch.setattr("config.Settings.model_config", {"env_file": None})

        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)  # Explicitly don't load from .env

        # Verify it's complaining about required fields
        assert (
            "openai_api_key" in str(exc_info.value).lower()
            or "pinecone_api_key" in str(exc_info.value).lower()
        )
