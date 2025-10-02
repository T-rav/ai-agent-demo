"""
Factory for creating mock vector store search results.
"""

from unittest.mock import AsyncMock


class VectorStoreSearchFactory:
    """Factory methods for creating vector store search mocks."""

    @staticmethod
    def create_mock_with_results(results):
        """
        Create a mock vector store that returns specified results.

        Args:
            results: List of (document, score) tuples to return

        Returns:
            Mock vector store with similarity_search_with_score method
        """
        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(return_value=results)
        return mock_vs

    @staticmethod
    def create_mock_with_empty_results():
        """Create a mock vector store that returns no results."""
        return VectorStoreSearchFactory.create_mock_with_results([])
