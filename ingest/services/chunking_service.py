"""
Document chunking service with structure - aware strategies.
Implements the Single Responsibility Principle and Strategy Pattern.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models import ChunkingError, ChunkMetadata, DocumentChunk, ProcessedDocument
from ..utils import MarkdownSectionSplitter, ParagraphSplitter, SentenceSplitter, TiktokenEncoder


class ChunkingStrategy(ABC):
    """Abstract base class for chunking strategies."""

    @abstractmethod
    def chunk(self, document: ProcessedDocument, chunker: "DocumentChunkingService") -> List[DocumentChunk]:
        """Chunk a document using this strategy."""


class MarkdownChunkingStrategy(ChunkingStrategy):
    """Chunking strategy for Markdown documents that respects structure."""

    def __init__(self) -> None:
        """Initialize the Markdown chunking strategy."""
        self._section_splitter = MarkdownSectionSplitter()

    def chunk(self, document: ProcessedDocument, chunker: "DocumentChunkingService") -> List[DocumentChunk]:
        """Chunk Markdown document respecting section structure."""
        chunks = []

        # Split by headers first
        sections = self._section_splitter.split(document.content)

        for section in sections:
            section_chunks = chunker._chunk_section(document, section)
            chunks.extend(section_chunks)

        return chunks


class PDFChunkingStrategy(ChunkingStrategy):
    """Chunking strategy for PDF documents that maintains page boundaries."""

    def chunk(self, document: ProcessedDocument, chunker: "DocumentChunkingService") -> List[DocumentChunk]:
        """Chunk PDF document with page awareness."""
        chunks = []

        # Split by pages first
        pages = document.content.split("--- Page ")

        for i, page_content in enumerate(pages):
            if not page_content.strip():
                continue

            # Add page number back for context
            if i > 0:
                page_content = f"--- Page {page_content}"

            page_num = i + 1 if i > 0 else 1
            page_chunks = chunker._chunk_text_content(document, page_content, page_num=page_num)
            chunks.extend(page_chunks)

        return chunks


class TextChunkingStrategy(ChunkingStrategy):
    """Chunking strategy for plain text documents."""

    def chunk(self, document: ProcessedDocument, chunker: "DocumentChunkingService") -> List[DocumentChunk]:
        """Chunk plain text document."""
        return chunker._chunk_text_content(document, document.content)


class DocumentChunkingService:
    """
    Service for chunking documents into smaller pieces suitable for embedding.

    Uses the Strategy pattern for different document types.
    Follows the Single Responsibility Principle.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        min_chunk_size: int = 100,
        max_chunk_size: int = 2000,
        token_encoder: Optional[TiktokenEncoder] = None,
    ) -> None:
        """
        Initialize the document chunking service.

        Args:
            chunk_size: Target tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
            min_chunk_size: Minimum chunk size in tokens
            max_chunk_size: Maximum chunk size in tokens
            token_encoder: Token encoder service
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self._token_encoder = token_encoder or TiktokenEncoder()

        # Initialize text splitters
        self._paragraph_splitter = ParagraphSplitter()
        self._sentence_splitter = SentenceSplitter()

        # Initialize chunking strategies
        self._strategies: Dict[str, ChunkingStrategy] = {
            ".md": MarkdownChunkingStrategy(),
            ".pdf": PDFChunkingStrategy(),
            ".txt": TextChunkingStrategy(),
        }

        # Initialize global chunk index
        self._global_chunk_index = 0

    def chunk_document(self, document: ProcessedDocument) -> List[DocumentChunk]:
        """
        Split a document into chunks using appropriate strategy.

        Args:
            document: Document to chunk

        Returns:
            List of document chunks

        Raises:
            ChunkingError: If chunking fails
        """
        try:
            if not document.content:
                return []

            # Reset global chunk index for this document
            self._global_chunk_index = 0

            file_type = document.file_type.value
            strategy = self._strategies.get(file_type, self._strategies[".txt"])

            return strategy.chunk(document, self)

        except Exception as e:
            raise ChunkingError(f"Failed to chunk document {document.file_name}: {e}") from e

    def _chunk_section(self, document: ProcessedDocument, section: Dict[str, Any]) -> List[DocumentChunk]:
        """Chunk a document section intelligently."""
        content = section["content"]
        header = section.get("header", "")

        # If section is small enough, keep as single chunk
        token_count = self._token_encoder.count_tokens(content)
        if token_count <= self.chunk_size:
            chunk = self._create_chunk(document, content, self._global_chunk_index, section_header=header)
            self._global_chunk_index += 1
            return [chunk]

        # Otherwise, chunk the content
        return self._chunk_text_content(document, content, section_header=header)

    def _chunk_text_content(
        self,
        document: ProcessedDocument,
        content: str,
        section_header: Optional[str] = None,
        page_num: Optional[int] = None,
    ) -> List[DocumentChunk]:
        """Chunk text content with semantic awareness."""
        # Split into paragraphs first (better than sentences for most content)
        paragraphs = self._paragraph_splitter.split(content)
        chunks: List[DocumentChunk] = []
        current_chunk: List[str] = []
        current_tokens = 0

        for paragraph in paragraphs:
            paragraph_tokens = self._token_encoder.count_tokens(paragraph)

            # If single paragraph is too large, split it further
            if paragraph_tokens > self.max_chunk_size:
                # Split large paragraph by sentences
                sentences = self._sentence_splitter.split(paragraph)
                for sentence in sentences:
                    sentence_tokens = self._token_encoder.count_tokens(sentence)

                    if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                        chunk_text = "\n\n".join(current_chunk)
                        chunks.append(
                            self._create_chunk(
                                document,
                                chunk_text,
                                self._global_chunk_index,
                                section_header=section_header,
                                page_num=page_num,
                            )
                        )
                        self._global_chunk_index += 1

                        # Start new chunk with overlap
                        overlap_text = self._get_overlap_text(chunk_text)
                        current_chunk = [overlap_text] if overlap_text else []
                        current_tokens = self._token_encoder.count_tokens("\n\n".join(current_chunk))

                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
            else:
                # Normal paragraph processing
                if current_tokens + paragraph_tokens > self.chunk_size and current_chunk:
                    chunk_text = "\n\n".join(current_chunk)
                    chunks.append(
                        self._create_chunk(
                            document,
                            chunk_text,
                            self._global_chunk_index,
                            section_header=section_header,
                            page_num=page_num,
                        )
                    )
                    self._global_chunk_index += 1

                    # Start new chunk with overlap
                    overlap_text = self._get_overlap_text(chunk_text)
                    current_chunk = [overlap_text] if overlap_text else []
                    current_tokens = self._token_encoder.count_tokens("\n\n".join(current_chunk))

                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens

        # Add final chunk if there's content
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            if self._token_encoder.count_tokens(chunk_text) >= self.min_chunk_size:
                chunks.append(
                    self._create_chunk(
                        document, chunk_text, self._global_chunk_index, section_header=section_header, page_num=page_num
                    )
                )
                self._global_chunk_index += 1

        return chunks

    def _get_overlap_text(self, chunk_text: str) -> str:
        """Get overlap text from the end of a chunk."""
        tokens = self._token_encoder.encode(chunk_text)
        if len(tokens) <= self.chunk_overlap:
            return chunk_text

        overlap_tokens = tokens[-self.chunk_overlap :]
        return self._token_encoder.decode(overlap_tokens)

    def _create_chunk(
        self,
        document: ProcessedDocument,
        chunk_text: str,
        chunk_index: int,
        section_header: Optional[str] = None,
        page_num: Optional[int] = None,
    ) -> DocumentChunk:
        """Create a chunk dictionary with enhanced metadata."""
        # Create unique chunk ID
        chunk_id = f"{document.file_name}_{chunk_index}"
        if section_header:
            # Clean section header for ID
            clean_header = re.sub(r"[^\w\s-]", "", section_header).strip()
            clean_header = re.sub(r"\s+", "_", clean_header)[:50]  # Limit length
            chunk_id = f"{document.file_name}_{clean_header}_{chunk_index}"

        metadata = ChunkMetadata(
            file_name=document.file_name,
            file_type=document.file_type,
            document_title=document.title,
            chunk_index=chunk_index,
            token_count=self._token_encoder.count_tokens(chunk_text),
            char_count=len(chunk_text),
            section_header=section_header,
            page_number=page_num,
        )

        return DocumentChunk(id=chunk_id, content=chunk_text, metadata=metadata)
