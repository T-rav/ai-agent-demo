"""
Services for the ingestion system.
"""

from .chunking_service import DocumentChunkingService
from .document_processor import SmartTextChunker  # Legacy - to be deprecated
from .document_processor_service import DocumentProcessorService
from .pinecone_client import PineconeVectorStore

__all__ = [
    "DocumentProcessorService",
    "DocumentChunkingService",
    "PineconeVectorStore",
    "SmartTextChunker",  # Legacy
]
