"""
Tests for utility functions and helpers.
"""

from unittest.mock import AsyncMock, patch

import pytest


class TestKnowledgeBaseSearchTool:
    """Tests for knowledge base search tool functionality."""

    @pytest.mark.asyncio
    async def test_search_knowledge_base_returns_formatted_results(self):
        """Test that search_knowledge_base returns formatted results."""
        from tests.builders import a_document
        from tests.factories.vector_store_search_factory import VectorStoreSearchFactory
        from tools import search_knowledge_base

        # Use builder with fluent syntax
        doc_with_score = (
            a_document()
            .with_content("RAG systems combine retrieval with generation.")
            .with_source("rag-intro.md")
            .with_title("RAG Introduction")
            .build_with_score()
        )

        # Use factory to create mock
        mock_vs = VectorStoreSearchFactory.create_mock_with_results([doc_with_score])

        with patch("tools.vector_store_service", mock_vs):
            result = await search_knowledge_base.ainvoke({"query": "What is RAG?"})

            assert "[KB-1]" in result
            assert "RAG Introduction" in result
            assert "rag-intro.md" in result

    @pytest.mark.asyncio
    async def test_search_knowledge_base_empty_results(self):
        """Test search_knowledge_base with no results."""
        from tests.factories.vector_store_search_factory import VectorStoreSearchFactory
        from tools import search_knowledge_base

        # Use factory to create empty results mock
        mock_vs = VectorStoreSearchFactory.create_mock_with_empty_results()

        with patch("tools.vector_store_service", mock_vs):
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
