"""
Additional tests for Settings validation and configuration.
"""



class TestSettingsDefaults:
    """Tests for Settings default values."""

    def test_settings_default_values(self, mock_env_vars):
        """Test that settings have correct defaults."""
        from config import Settings

        settings = Settings()

        assert settings.openai_model == "gpt-4-turbo-preview"
        assert settings.pinecone_index_name == "test-index"
        assert settings.embedding_model == "text-embedding-3-small"
        assert settings.embedding_dimensions == 1536
        assert settings.retrieval_k == 5

    def test_settings_debug_mode(self, mock_env_vars):
        """Test debug mode setting."""
        from config import Settings

        settings = Settings()

        assert settings.debug is True  # Set to true in mock_env_vars

    def test_settings_langchain_tracing(self, mock_env_vars):
        """Test LangChain tracing configuration."""
        from config import Settings

        settings = Settings()

        assert hasattr(settings, "langchain_tracing_v2")
        assert hasattr(settings, "langchain_project")


class TestSettingsCustomValues:
    """Tests for Settings with custom values."""

    def test_settings_custom_model(self, monkeypatch):
        """Test settings with custom OpenAI model."""
        from config import Settings

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-4")
        monkeypatch.setenv("PINECONE_API_KEY", "test-key")
        monkeypatch.setenv("PINECONE_ENVIRONMENT", "test-env")

        settings = Settings()

        assert settings.openai_model == "gpt-4"

    def test_settings_custom_retrieval_k(self, monkeypatch):
        """Test settings with custom retrieval k."""
        from config import Settings

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("PINECONE_API_KEY", "test-key")
        monkeypatch.setenv("PINECONE_ENVIRONMENT", "test-env")
        monkeypatch.setenv("RETRIEVAL_K", "10")

        settings = Settings()

        assert settings.retrieval_k == 10

    def test_settings_custom_embedding_dimensions(self, monkeypatch):
        """Test settings with custom embedding dimensions."""
        from config import Settings

        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("PINECONE_API_KEY", "test-key")
        monkeypatch.setenv("PINECONE_ENVIRONMENT", "test-env")
        monkeypatch.setenv("EMBEDDING_DIMENSIONS", "3072")

        settings = Settings()

        assert settings.embedding_dimensions == 3072
