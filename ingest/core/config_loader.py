"""
Configuration loader for the ingestion system.
Reads configuration from pyproject.toml and environment variables using Pydantic.
"""

import os
import tomllib
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from ..models import ConfigurationError, IngestionConfig


class Config:
    """Configuration manager for the ingestion system."""

    def __init__(self, config_file: str = "pyproject.toml"):
        """
        Initialize configuration from pyproject.toml and environment variables.

        Args:
            config_file: Path to the pyproject.toml file
        """
        # Load .env file if it exists
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)

        self.config_file = Path(config_file)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from pyproject.toml file."""
        if not self.config_file.exists():
            raise FileNotFoundError("Configuration file not found: {self.config_file}")

        with open(self.config_file, "rb") as f:
            toml_data = tomllib.load(f)

        # Extract our configuration section
        config_section = toml_data.get("tool", {}).get("ai-agent-demo", {})

        if not config_section:
            raise ValueError("No [tool.ai-agent-demo] section found in pyproject.toml")

        return config_section

    def get_api_config(self) -> Dict[str, str]:
        """Get API configuration with environment variable overrides."""
        api_config = self._config.get("api", {})

        return {
            "openai_api_key": os.getenv("OPENAI_API_KEY", api_config.get("openai_api_key", "")),
            "pinecone_api_key": os.getenv(
                "PINECONE_API_KEY", api_config.get("pinecone_api_key", "")
            ),
            "pinecone_environment": os.getenv(
                "PINECONE_ENVIRONMENT", api_config.get("pinecone_environment", "")
            ),
        }

    def get_database_config(self) -> Dict[str, str]:
        """Get database configuration."""
        db_config = self._config.get("database", {})

        return {
            "index_name": os.getenv(
                "PINECONE_INDEX_NAME",
                db_config.get("index_name", "ai-agent-demo-index"),
            )
        }

    def get_embedding_config(self) -> Dict[str, Any]:
        """Get embedding configuration."""
        embedding_config = self._config.get("embedding", {})

        return {
            "model": os.getenv(
                "EMBEDDING_MODEL",
                embedding_config.get("model", "text - embedding - 3-small"),
            ),
            "dimensions": int(
                os.getenv(
                    "EMBEDDING_DIMENSIONS",
                    str(embedding_config.get("dimensions", 1536)),
                )
            ),
        }

    def get_processing_config(self) -> Dict[str, int]:
        """Get processing configuration."""
        processing_config = self._config.get("processing", {})

        return {
            "chunk_size": int(
                os.getenv("CHUNK_SIZE", str(processing_config.get("chunk_size", 1000)))
            ),
            "chunk_overlap": int(
                os.getenv("CHUNK_OVERLAP", str(processing_config.get("chunk_overlap", 200)))
            ),
            "embedding_batch_size": int(
                os.getenv(
                    "EMBEDDING_BATCH_SIZE",
                    str(processing_config.get("embedding_batch_size", 100)),
                )
            ),
            "upsert_batch_size": int(
                os.getenv(
                    "UPSERT_BATCH_SIZE",
                    str(processing_config.get("upsert_batch_size", 100)),
                )
            ),
        }

    def get_paths_config(self) -> Dict[str, str]:
        """Get paths configuration."""
        paths_config = self._config.get("paths", {})

        return {
            "corpus_path": os.getenv(
                "CORPUS_PATH", paths_config.get("corpus_path", "../data/corpus")
            )
        }

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        logging_config = self._config.get("logging", {})

        return {
            "level": os.getenv("LOG_LEVEL", logging_config.get("level", "INFO")),
            "show_progress": os.getenv(
                "SHOW_PROGRESS", str(logging_config.get("show_progress", True))
            ).lower()
            == "true",
        }

    def get_all_config(self) -> Dict[str, Any]:
        """Get complete configuration dictionary."""
        return {
            **self.get_api_config(),
            **self.get_database_config(),
            **self.get_embedding_config(),
            **self.get_processing_config(),
            **self.get_paths_config(),
            **self.get_logging_config(),
        }

    def validate_required_config(self) -> None:
        """Validate that all required configuration is present."""
        api_config = self.get_api_config()

        required_fields = [
            ("openai_api_key", "OPENAI_API_KEY"),
            ("pinecone_api_key", "PINECONE_API_KEY"),
            ("pinecone_environment", "PINECONE_ENVIRONMENT"),
        ]

        missing_fields = []
        for field, env_var in required_fields:
            value = api_config.get(field, "")
            if not value or value == "your_{field}_here":
                missing_fields.append("{field} (set via {env_var} environment variable)")

        if missing_fields:
            raise ValueError("Missing required configuration: {', '.join(missing_fields)}")


def load_config(config_file: str = "pyproject.toml") -> IngestionConfig:
    """
    Convenience function to load and validate configuration using Pydantic.

    Args:
        config_file: Path to the pyproject.toml file

    Returns:
        Validated IngestionConfig instance

    Raises:
        ConfigurationError: If configuration is invalid or missing
    """
    try:
        config = Config(config_file)
        config.validate_required_config()
        config_dict = config.get_all_config()

        # Create Pydantic model with validation
        return IngestionConfig(**config_dict)

    except Exception as e:
        raise ConfigurationError(f"Failed to load configuration: {e}") from e
