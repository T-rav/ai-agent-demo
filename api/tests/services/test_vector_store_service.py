"""
Tests for VectorStoreService.
Testing vector store interactions and search functionality.
"""

from unittest.mock import MagicMock, patch

import pytest


class TestVectorStoreServiceInitialization:
    """Tests for vector store service initialization."""

    @pytest.fixture
    def mock_pinecone(self):
        """Mock Pinecone client."""
        with patch("vector_store.Pinecone") as mock:
            yield mock

    @pytest.fixture
    def mock_embeddings(self):
        """Mock OpenAI embeddings."""
        with patch("vector_store.OpenAIEmbeddings") as mock:
            yield mock

    @pytest.fixture
    def mock_langchain_pinecone(self):
        """Mock LangChain Pinecone."""
        with patch("vector_store.LangchainPinecone") as mock:
            yield mock

    def test_vector_store_initialization(self, mock_env_vars, mock_pinecone, mock_embeddings):
        """Test vector store service initialization."""
        from vector_store import VectorStoreService

        service = VectorStoreService()

        assert service.index_name == "test-index"
        assert service._vectorstore is None

    def test_vectorstore_property(
        self, mock_env_vars, mock_pinecone, mock_embeddings, mock_langchain_pinecone
    ):
        """Test vectorstore property creates instance."""
        from vector_store import VectorStoreService

        mock_vs = MagicMock()
        mock_langchain_pinecone.from_existing_index.return_value = mock_vs

        service = VectorStoreService()
        vectorstore = service.vectorstore

        assert vectorstore == mock_vs
        mock_langchain_pinecone.from_existing_index.assert_called_once()


class TestVectorStoreServiceSingleton:
    """Tests for vector store service singleton instance."""

    def test_vector_store_service_singleton(self, mock_env_vars):
        """Test that vector_store_service is a singleton instance."""
        from vector_store import VectorStoreService, vector_store_service

        assert isinstance(vector_store_service, VectorStoreService)
