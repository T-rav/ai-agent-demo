"""
Custom exceptions for the ingestion system.
"""


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    pass


class ProcessingError(Exception):
    """Raised when document processing fails."""

    pass


class ChunkingError(Exception):
    """Raised when document chunking fails."""

    pass


class VectorStoreError(Exception):
    """Raised when vector store operations fail."""

    pass
