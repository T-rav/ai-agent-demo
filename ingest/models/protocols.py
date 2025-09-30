"""
Protocol definitions for the ingestion system.
"""

from typing import List, Dict, Any, Optional, Protocol
from pathlib import Path

from .document import ProcessedDocument
from .chunk import DocumentChunk
from .search import SearchResult


class TokenEncoder(Protocol):
    """Protocol for token encoding/decoding."""
    
    def encode(self, text: str) -> List[int]:
        """Encode text to tokens."""
        ...
    
    def decode(self, tokens: List[int]) -> str:
        """Decode tokens to text."""
        ...


class DocumentProcessor(Protocol):
    """Protocol for document processing."""
    
    def process_file(self, file_path: Path) -> Optional[ProcessedDocument]:
        """Process a single file."""
        ...


class TextChunker(Protocol):
    """Protocol for text chunking."""
    
    def chunk_document(self, document: ProcessedDocument) -> List[DocumentChunk]:
        """Chunk a document into smaller pieces."""
        ...


class TitleExtractor(Protocol):
    """Protocol for title extraction."""
    
    def extract_title(self, file_path: Path, content: str) -> str:
        """Extract title from document content."""
        ...


class VectorStore(Protocol):
    """Protocol for vector storage operations."""
    
    def create_index_if_not_exists(self) -> None:
        """Create index if it doesn't exist."""
        ...
    
    def upsert_chunks(self, chunks: List[DocumentChunk], batch_size: int = 100) -> None:
        """Upsert chunks to the vector store."""
        ...
    
    def query_similar(self, query_text: str, top_k: int = 10) -> List[SearchResult]:
        """Query for similar vectors."""
        ...
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        ...
