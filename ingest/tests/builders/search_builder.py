"""
Fluent builder for SearchResult objects.
"""

from typing import Any, Dict

from ...models import SearchResult


class SearchResultBuilder:
    """Fluent builder for SearchResult objects."""

    def __init__(self):
        self._chunk_id = "test - chunk - 1"
        self._content = "Sample search result content"
        self._score = 0.85
        self._metadata = {}

    def with_chunk_id(self, chunk_id: str) -> "SearchResultBuilder":
        """Set the chunk ID."""
        self._chunk_id = chunk_id
        return self

    def with_content(self, content: str) -> "SearchResultBuilder":
        """Set the content."""
        self._content = content
        return self

    def with_score(self, score: float) -> "SearchResultBuilder":
        """Set the similarity score."""
        self._score = score
        return self

    def with_metadata(self, metadata: Dict[str, Any]) -> "SearchResultBuilder":
        """Set the metadata."""
        self._metadata = metadata
        return self

    def with_high_score(self) -> "SearchResultBuilder":
        """Set a high similarity score."""
        return self.with_score(0.95)

    def with_low_score(self) -> "SearchResultBuilder":
        """Set a low similarity score."""
        return self.with_score(0.45)

    def build(self) -> SearchResult:
        """Build the SearchResult."""
        return SearchResult(id=self._chunk_id, score=self._score, metadata=self._metadata)
