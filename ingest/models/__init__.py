"""
Pydantic models for the ingestion system.
Provides data validation, serialization, and type safety.
"""

from .document import ProcessedDocument, DocumentMetadata
from .chunk import DocumentChunk, ChunkMetadata
from .search import SearchResult
from .config import IngestionConfig
from .enums import FileType
from .exceptions import (
    ProcessingError,
    ChunkingError,
    VectorStoreError,
    ConfigurationError
)
from .protocols import (
    TokenEncoder,
    DocumentProcessor,
    TextChunker,
    TitleExtractor,
    VectorStore
)

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
