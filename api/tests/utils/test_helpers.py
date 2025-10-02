"""
Tests for utility functions and helpers.
"""

from unittest.mock import patch

import pytest

from ..factories import VectorStoreFactory


class TestKnowledgeBaseSearchTool:
    """Tests for knowledge base search tool functionality."""

    @pytest.mark.asyncio
    async def test_search_knowledge_base_returns_formatted_results(self):
        """Test that search_knowledge_base returns formatted results."""
        from tools import search_knowledge_base

        # Use factory directly - no fixture needed
        mock_vector_store = VectorStoreFactory.create_mock_vector_store()

        with patch("tools.vector_store_service", mock_vector_store):
            result = await search_knowledge_base.ainvoke({"query": "What is RAG?"})

            assert "RAG systems combine retrieval" in result
            assert "[KB-1]" in result
            assert "KNOWLEDGE BASE SOURCES" in result
            mock_vector_store.similarity_search_with_score.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_knowledge_base_empty_results(self):
        """Test search_knowledge_base with no results."""
        from tools import search_knowledge_base

        # Use factory directly - no fixture needed
        empty_vector_store = VectorStoreFactory.create_empty_vector_store()

        with patch("tools.vector_store_service", empty_vector_store):
            result = await search_knowledge_base.ainvoke({"query": "Unknown topic"})

            assert "No relevant information found" in result


class TestConfigurationHelpers:
    """Tests for configuration helper functions."""

    def test_settings_singleton_pattern(self):
        """Test that settings can be imported and used."""
        from config import settings

        assert settings is not None
        assert hasattr(settings, "openai_api_key")
        assert hasattr(settings, "pinecone_api_key")

    def test_settings_has_all_required_fields(self):
        """Test that settings object has all required configuration."""
        from config import settings

        # These should not raise AttributeError
        _ = settings.openai_api_key
        _ = settings.openai_model
        _ = settings.pinecone_api_key
        _ = settings.pinecone_environment
        _ = settings.pinecone_index_name
        _ = settings.embedding_model
        _ = settings.embedding_dimensions
        _ = settings.retrieval_k

    def test_settings_score_threshold(self):
        """Test that settings has score threshold."""
        from config import settings

        assert hasattr(settings, "score_threshold")
        assert settings.score_threshold >= 0
        assert settings.score_threshold <= 1
