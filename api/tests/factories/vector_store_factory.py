"""
Factory for creating vector store test doubles.
"""

from unittest.mock import AsyncMock

from langchain_core.documents import Document


class VectorStoreFactory:
    """Factory methods for creating vector store test doubles."""

    @staticmethod
    def create_mock_vector_store():
        """Create a mock vector store service."""
        mock = AsyncMock()

        # Default documents for similarity search
        mock_doc1 = Document(
            page_content="RAG systems combine retrieval with generation.",
            metadata={
                "source": "rag_overview.md",
                "title": "RAG Systems Overview",
                "chunk_index": 0,
            },
        )
        mock_doc2 = Document(
            page_content="Vector databases store embeddings efficiently.",
            metadata={
                "source": "vector_db.md",
                "title": "Vector Databases",
                "chunk_index": 1,
            },
        )

        # Mock similarity_search_with_score
        mock.similarity_search_with_score = AsyncMock(
            return_value=[(mock_doc1, 0.85), (mock_doc2, 0.78)]
        )

        # Mock similarity_search
        mock.similarity_search = AsyncMock(return_value=[mock_doc1, mock_doc2])

        return mock

    @staticmethod
    def create_empty_vector_store():
        """Create a mock vector store with no results."""
        mock = AsyncMock()

        mock.similarity_search_with_score = AsyncMock(return_value=[])
        mock.similarity_search = AsyncMock(return_value=[])

        return mock

    @staticmethod
    def create_vector_store_with_custom_docs(documents):
        """Create a mock vector store with custom documents."""
        mock = AsyncMock()

        docs_with_scores = [(doc, 0.9 - i * 0.1) for i, doc in enumerate(documents)]

        mock.similarity_search_with_score = AsyncMock(return_value=docs_with_scores)
        mock.similarity_search = AsyncMock(return_value=documents)

        return mock
