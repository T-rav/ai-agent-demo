"""
AI Agent Demo - Document Ingestion System

A modern, well-architected document ingestion system following SOLID principles.
"""

from .models import (
    ProcessedDocument,
    DocumentChunk,
    SearchResult,
    DocumentMetadata,
    ChunkMetadata,
    ProcessingError,
    ChunkingError,
    VectorStoreError,
    ConfigurationError
)

from .services import DocumentProcessorService, DocumentChunkingService, PineconeVectorStore
from .utils import DocumentTitleExtractor, DocumentContentExtractor, TextCleaner, TiktokenEncoder, SentenceSplitter, ParagraphSplitter, MarkdownSectionSplitter
from .core import load_config, CorpusIngester

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
