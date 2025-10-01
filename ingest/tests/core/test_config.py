"""
Tests for the config_loader module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from ...core import load_config
from ...models import ConfigurationError, IngestionConfig


class TestConfigLoader:
    """Test cases for config loading functionality."""

    def test_load_config_with_env_vars(self):
        """Test loading config with environment variables."""
        env_vars = {
            "OPENAI_API_KEY": "test - openai - key",
            "PINECONE_API_KEY": "test - pinecone - key",
            "PINECONE_ENVIRONMENT": "test - env",
            "DATABASE_INDEX_NAME": "test - index",
            "EMBEDDING_MODEL": "text - embedding - 3-large",
            "EMBEDDING_DIMENSIONS": "3072",
            "CHUNK_SIZE": "1500",
            "CHUNK_OVERLAP": "300",
        }

        from ingest.tests.factories.config_factory import ConfigFactory

        with patch.dict(os.environ, env_vars):
            with patch("ingest.core.config_loader.Config.__init__") as mock_init:
                # Use factory to create mock config
                mock_config = ConfigFactory.create_mock_config()
                # Override with specific test values
                mock_config.get_all_config.return_value.update(
                    {
                        "openai_api_key": "test - openai - key",
                        "pinecone_api_key": "test - pinecone - key",
                        "model": "text - embedding - 3-large",
                        "dimensions": 3072,
                        "chunk_size": 1500,
                        "chunk_overlap": 300,
                    }
                )
                mock_init.return_value = None

                with patch("ingest.core.config_loader.Config", return_value=mock_config):
                    config = load_config()

                    assert isinstance(config, IngestionConfig)
                    assert config.openai_api_key == "test - openai - key"
                    assert config.pinecone_api_key == "test - pinecone - key"
                    assert config.pinecone_environment == "test - env"
                    assert config.index_name == "test - index"
                    assert config.model == "text - embedding - 3-large"
                    assert config.dimensions == 3072
                    assert config.chunk_size == 1500
                    assert config.chunk_overlap == 300

    def test_load_config_missing_required_env_vars(self):
        """Test that missing required environment variables raise an error."""
        # Clear any existing env vars
        env_vars = {
            "OPENAI_API_KEY": "",
            "PINECONE_API_KEY": "",
            "PINECONE_ENVIRONMENT": "",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            with pytest.raises(ConfigurationError, match="Failed to load configuration"):
                load_config()

    def test_load_config_with_pyproject_toml(self):
        """Test loading config from pyproject.toml file."""
        toml_content = """
[tool.ai - agent - demo.api]
openai_api_key = ""
pinecone_api_key = ""
pinecone_environment = ""

[tool.ai - agent - demo.database]
index_name = "test - index - from - toml"

[tool.ai - agent - demo.embedding]
model = "text - embedding - 3-small"
dimensions = 1536

[tool.ai - agent - demo.processing]
chunk_size = 800
chunk_overlap = 150
min_chunk_size = 50
max_chunk_size = 1200

[tool.ai - agent - demo.paths]
corpus_path = "test / corpus"

[tool.ai - agent - demo.logging]
level = "DEBUG"
show_progress = false
"""

        env_vars = {
            "OPENAI_API_KEY": "env - openai - key",
            "PINECONE_API_KEY": "env - pinecone - key",
            "PINECONE_ENVIRONMENT": "env - environment",
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(toml_content)
            f.flush()

            try:
                with patch.dict(os.environ, env_vars):
                    with patch("pathlib.Path.cwd") as mock_cwd:
                        mock_cwd.return_value = Path(f.name).parent
                        with patch("pathlib.Path.exists") as mock_exists:
                            mock_exists.return_value = True
                with patch("ingest.core.config_loader.Config.__init__") as mock_init:
                    # Use factory
                    from ingest.tests.factories.config_factory import ConfigFactory

                    mock_config = ConfigFactory.create_mock_config()
                    mock_config.get_all_config.return_value.update(
                        {
                            "openai_api_key": "env - openai - key",
                            "pinecone_api_key": "env - pinecone - key",
                            "pinecone_environment": "env - environment",
                            "index_name": "test - index - from - toml",
                            "chunk_size": 800,
                            "chunk_overlap": 150,
                            "min_chunk_size": 50,
                            "max_chunk_size": 1200,
                            "level": "DEBUG",
                            "show_progress": False,
                        }
                    )
                    mock_init.return_value = None

                    with patch("ingest.core.config_loader.Config", return_value=mock_config):
                        config = load_config()

                        # Environment variables should override TOML
                        assert config.openai_api_key == "env - openai - key"
                        assert config.pinecone_api_key == "env - pinecone - key"
                        assert config.pinecone_environment == "env - environment"

                        # TOML values should be used for non - env settings
                        assert config.index_name == "test - index - from - toml"
                        assert config.chunk_size == 800
                        assert config.chunk_overlap == 150
                        assert config.corpus_path == "test / corpus"
                        assert config.level == "DEBUG"
                        assert config.show_progress is False
            finally:
                os.unlink(f.name)

    def test_load_config_defaults(self):
        """Test that default values are used when not specified."""
        env_vars = {
            "OPENAI_API_KEY": "test - key",
            "PINECONE_API_KEY": "test - key",
            "PINECONE_ENVIRONMENT": "test - env",
        }

        with patch.dict(os.environ, env_vars):
            with patch("ingest.core.config_loader.Config.__init__") as mock_init:
                # Use factory
                from ingest.tests.factories.config_factory import ConfigFactory

                mock_config = ConfigFactory.create_mock_config()
                mock_config.get_all_config.return_value.update(
                    {
                        "index_name": "ai - agent - demo - index",
                    }
                )
                mock_init.return_value = None

                with patch("ingest.core.config_loader.Config", return_value=mock_config):
                    config = load_config()

                    # Check defaults
                    assert config.index_name == "ai - agent - demo - index"
                    assert config.model == "text - embedding - 3-small"
                    assert config.dimensions == 1536
                    assert config.chunk_size == 1000
                    assert config.chunk_overlap == 200
                    assert config.corpus_path == "data / corpus"
                    assert config.level == "INFO"
                    assert config.show_progress is True

    def test_load_config_invalid_toml(self):
        """Test handling of invalid TOML file."""
        invalid_toml = "invalid toml content ["

        env_vars = {
            "OPENAI_API_KEY": "test - key",
            "PINECONE_API_KEY": "test - key",
            "PINECONE_ENVIRONMENT": "test - env",
        }

        with patch.dict(os.environ, env_vars):
            with patch("pathlib.Path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=invalid_toml.encode())):
                    with pytest.raises(ConfigurationError, match="Failed to load configuration"):
                        load_config()

    def test_load_config_with_dotenv(self):
        """Test loading config with .env file."""
        env_content = """
OPENAI_API_KEY=dotenv - openai - key
PINECONE_API_KEY=dotenv - pinecone - key
PINECONE_ENVIRONMENT=dotenv - env
CHUNK_SIZE=2000
"""

        with patch("pathlib.Path.exists") as mock_exists:

            def exists_side_effect(path):
                if str(path) == "pyproject.toml":
                    return False
                elif str(path) == ".env":
                    return True
                return False

            mock_exists.side_effect = exists_side_effect

            with patch("builtins.open", mock_open(read_data=env_content)):
                with patch("dotenv.load_dotenv") as mock_load_dotenv:
                    mock_load_dotenv.return_value = True

                    # Mock the environment after dotenv loads
                    env_vars = {
                        "OPENAI_API_KEY": "dotenv - openai - key",
                        "PINECONE_API_KEY": "dotenv - pinecone - key",
                        "PINECONE_ENVIRONMENT": "dotenv - env",
                        "CHUNK_SIZE": "2000",
                    }

                    with patch.dict(os.environ, env_vars):
                        with patch("ingest.core.config_loader.Config.__init__") as mock_init:
                            # Use factory
                            from ingest.tests.factories.config_factory import (
                                ConfigFactory,
                            )

                            mock_config = ConfigFactory.create_mock_config()
                            mock_config.get_all_config.return_value.update(
                                {
                                    "openai_api_key": "dotenv - openai - key",
                                    "pinecone_api_key": "dotenv - pinecone - key",
                                    "pinecone_environment": "dotenv - env",
                                    "chunk_size": 2000,
                                }
                            )
                            mock_init.return_value = None

                            with patch(
                                "ingest.core.config_loader.Config",
                                return_value=mock_config,
                            ):
                                config = load_config()

                                assert config.openai_api_key == "dotenv - openai - key"
                                assert config.pinecone_api_key == "dotenv - pinecone - key"
                                assert config.pinecone_environment == "dotenv - env"
                                assert config.chunk_size == 2000
