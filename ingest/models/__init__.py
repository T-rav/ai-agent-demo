"""
Pydantic models for the ingestion system.
Provides data validation, serialization, and type safety.
"""

from .chunk import ChunkMetadata, DocumentChunk
from .config import IngestionConfig
from .document import DocumentMetadata, ProcessedDocument
from .enums import FileType
from .exceptions import ChunkingError, ConfigurationError, ProcessingError, VectorStoreError
from .protocols import DocumentProcessor, TextChunker, TitleExtractor, TokenEncoder, VectorStore
from .search import SearchResult

__all__ = [
    # Data Models
    "ProcessedDocument",
    "DocumentMetadata",
    "DocumentChunk",
    "ChunkMetadata",
    "SearchResult",
    "IngestionConfig",
    # Enums
    "FileType",
    # Exceptions
    "ProcessingError",
    "ChunkingError",
    "VectorStoreError",
    "ConfigurationError",
    # Protocols
    "TokenEncoder",
    "DocumentProcessor",
    "TextChunker",
    "TitleExtractor",
    "VectorStore",
]
