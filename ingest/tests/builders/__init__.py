"""
Fluent data builders for test objects using a().b() syntax.
Each builder is in its own file following the one - class - per - file principle.
"""

from .chunk_builder import DocumentChunkBuilder
from .config_builder import IngestionConfigBuilder
from .document_builder import ProcessedDocumentBuilder
from .search_builder import SearchResultBuilder


# Convenience functions for creating builders with fluent syntax
def a_processed_document() -> ProcessedDocumentBuilder:
    """Create a ProcessedDocument builder."""
    return ProcessedDocumentBuilder()


def a_document_chunk() -> DocumentChunkBuilder:
    """Create a DocumentChunk builder."""
    return DocumentChunkBuilder()


def an_ingestion_config() -> IngestionConfigBuilder:
    """Create an IngestionConfig builder."""
    return IngestionConfigBuilder()


def a_search_result() -> SearchResultBuilder:
    """Create a SearchResult builder."""
    return SearchResultBuilder()


# Convenience functions for common test scenarios
def a_markdown_document() -> ProcessedDocumentBuilder:
    """Create a markdown document builder."""
    return a_processed_document().as_markdown()


def a_pdf_document() -> ProcessedDocumentBuilder:
    """Create a PDF document builder."""
    return a_processed_document().as_pdf()


def a_text_document() -> ProcessedDocumentBuilder:
    """Create a text document builder."""
    return a_processed_document().as_text()


def a_large_document() -> ProcessedDocumentBuilder:
    """Create a large document builder."""
    return a_processed_document().with_long_content()


def an_empty_document() -> ProcessedDocumentBuilder:
    """Create an empty document builder."""
    return a_processed_document().with_empty_content()


def a_markdown_chunk() -> DocumentChunkBuilder:
    """Create a markdown chunk builder."""
    return a_document_chunk().from_markdown_section("Introduction")


def a_pdf_chunk() -> DocumentChunkBuilder:
    """Create a PDF chunk builder."""
    return a_document_chunk().from_pdf_page(1)


def a_production_config() -> IngestionConfigBuilder:
    """Create a production config builder."""
    return an_ingestion_config().for_production()


def a_development_config() -> IngestionConfigBuilder:
    """Create a development config builder."""
    return an_ingestion_config().for_development()


def a_high_score_result() -> SearchResultBuilder:
    """Create a high - score search result builder."""
    return a_search_result().with_high_score()


def a_low_score_result() -> SearchResultBuilder:
    """Create a low - score search result builder."""
    return a_search_result().with_low_score()


__all__ = [
    "ProcessedDocumentBuilder",
    "DocumentChunkBuilder",
    "IngestionConfigBuilder",
    "SearchResultBuilder",
    "a_processed_document",
    "a_document_chunk",
    "an_ingestion_config",
    "a_search_result",
    "a_markdown_document",
    "a_pdf_document",
    "a_text_document",
    "a_large_document",
    "an_empty_document",
    "a_markdown_chunk",
    "a_pdf_chunk",
    "a_production_config",
    "a_development_config",
    "a_high_score_result",
    "a_low_score_result",
]
