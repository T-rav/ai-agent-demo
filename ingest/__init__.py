"""
AI Agent Demo - Document Ingestion System

A modern, well - architected document ingestion system following SOLID principles.
"""

from .models import (
    ChunkingError,
    ChunkMetadata,
    ConfigurationError,
    DocumentChunk,
    DocumentMetadata,
    ProcessedDocument,
    ProcessingError,
    SearchResult,
    VectorStoreError,
)
from .services import DocumentChunkingService, DocumentProcessorService
from .utils import (
    DocumentContentExtractor,
    DocumentTitleExtractor,
    MarkdownSectionSplitter,
    ParagraphSplitter,
    SentenceSplitter,
    TextCleaner,
    TiktokenEncoder,
)

__version__ = "0.1.0"
__all__ = [
    # Types
    "ProcessedDocument",
    "DocumentChunk",
    "SearchResult",
    "DocumentMetadata",
    "ChunkMetadata",
    # Exceptions
    "ProcessingError",
    "ChunkingError",
    "VectorStoreError",
    "ConfigurationError",
    # Services
    "DocumentProcessorService",
    "DocumentChunkingService",
    "DocumentTitleExtractor",
    "DocumentContentExtractor",
    "TextCleaner",
    "TiktokenEncoder",
    # Utilities
    "SentenceSplitter",
    "ParagraphSplitter",
    "MarkdownSectionSplitter",
]
