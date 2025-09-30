"""
Factory for creating configuration test doubles.
"""

from unittest.mock import Mock


class ConfigFactory:
    """Factory methods for creating configuration test doubles."""

    @staticmethod
    def create_mock_config() -> Mock:
        """Create a mock configuration object."""
        config = Mock()
        config.validate_required_config.return_value = None
        config.get_all_config.return_value = {
            "openai_api_key": "test - key",
            "pinecone_api_key": "test - key",
            "pinecone_environment": "test - env",
            "index_name": "test - index",
            "model": "text - embedding - 3-small",
            "dimensions": 1536,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "min_chunk_size": 100,
            "max_chunk_size": 2000,
            "embedding_batch_size": 100,
            "upsert_batch_size": 100,
            "corpus_path": "data / corpus",
            "level": "INFO",
            "show_progress": True,
        }
        return config
