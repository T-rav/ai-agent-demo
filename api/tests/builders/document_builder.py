"""
Builder for creating mock documents in tests.
Uses fluent interface pattern.
"""

from typing import Dict
from unittest.mock import MagicMock


class DocumentBuilder:
    """Fluent builder for creating mock LangChain documents."""

    def __init__(self):
        """Initialize builder with default values."""
        self._page_content = "Default document content"
        self._metadata = {"source": "default.md", "title": "Default Title"}
        self._score = 0.95

    def with_content(self, content: str) -> "DocumentBuilder":
        """Set document content."""
        self._page_content = content
        return self

    def with_source(self, source: str) -> "DocumentBuilder":
        """Set source file."""
        self._metadata["source"] = source
        return self

    def with_title(self, title: str) -> "DocumentBuilder":
        """Set document title."""
        self._metadata["title"] = title
        return self

    def with_metadata(self, metadata: Dict) -> "DocumentBuilder":
        """Set complete metadata dictionary."""
        self._metadata = metadata
        return self

    def with_score(self, score: float) -> "DocumentBuilder":
        """Set relevance score."""
        self._score = score
        return self

    def build(self) -> MagicMock:
        """Build the mock document."""
        doc = MagicMock()
        doc.page_content = self._page_content
        doc.metadata = self._metadata
        return doc

    def build_with_score(self) -> tuple:
        """Build document with score tuple (doc, score)."""
        doc = self.build()
        return (doc, self._score)


def a_document() -> DocumentBuilder:
    """Create a document builder with default RAG content."""
    return (
        DocumentBuilder()
        .with_content("RAG systems combine retrieval with generation.")
        .with_source("rag-intro.md")
        .with_title("RAG Introduction")
    )


def an_empty_document() -> DocumentBuilder:
    """Create a document builder with minimal content."""
    return DocumentBuilder().with_content("").with_metadata({})


def a_kb_document() -> DocumentBuilder:
    """Create a knowledge base document builder."""
    return (
        DocumentBuilder()
        .with_content("Knowledge base content about AI and computing.")
        .with_source("kb-doc.md")
        .with_title("KB Document")
    )
