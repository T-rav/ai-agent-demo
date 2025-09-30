"""
Custom exceptions for the ingestion system.
"""


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""


class ProcessingError(Exception):
    """Raised when document processing fails."""


class ChunkingError(Exception):
    """Raised when document chunking fails."""


class VectorStoreError(Exception):
    """Raised when vector store operations fail."""

