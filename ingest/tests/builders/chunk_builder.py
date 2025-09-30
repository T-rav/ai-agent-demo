"""
Fluent builder for DocumentChunk objects.
"""

from ...models import DocumentChunk, ChunkMetadata, FileType


class DocumentChunkBuilder:
    """Fluent builder for DocumentChunk objects."""
    
    def __init__(self):
        self._id = "test-chunk-1"
        self._content = "Sample chunk content"
        self._metadata = ChunkMetadata(
            file_path="/test/document.md",
            file_name="document.md",
            file_type=FileType.MARKDOWN,
            document_title="Test Document",
            chunk_index=0,
            token_count=5,
            char_count=20,
            section_header=None,
            page_number=None
        )
    
    def with_id(self, chunk_id: str) -> 'DocumentChunkBuilder':
        """Set the chunk ID."""
        self._id = chunk_id
        return self
    
    def with_content(self, content: str) -> 'DocumentChunkBuilder':
        """Set the chunk content."""
        self._content = content
        return self
    
    def with_token_count(self, count: int) -> 'DocumentChunkBuilder':
        """Set the token count."""
        self._metadata.token_count = count
        return self
    
    def with_char_count(self, count: int) -> 'DocumentChunkBuilder':
        """Set the character count."""
        self._metadata.char_count = count
        return self
    
    def with_chunk_index(self, index: int) -> 'DocumentChunkBuilder':
        """Set the chunk index."""
        self._metadata.chunk_index = index
        return self
    
    def with_metadata(self, metadata: ChunkMetadata) -> 'DocumentChunkBuilder':
        """Set the chunk metadata."""
        self._metadata = metadata
        return self
    
    def with_document_title(self, title: str) -> 'DocumentChunkBuilder':
        """Set the document title in metadata."""
        self._metadata.document_title = title
        return self
    
    def with_section_header(self, header: str) -> 'DocumentChunkBuilder':
        """Set the section header in metadata."""
        self._metadata.section_header = header
        return self
    
    def with_page_number(self, page: int) -> 'DocumentChunkBuilder':
        """Set the page number in metadata."""
        self._metadata.page_number = page
        return self
    
    def from_markdown_section(self, header: str) -> 'DocumentChunkBuilder':
        """Configure as a markdown section chunk."""
        self._metadata.file_type = FileType.MARKDOWN
        self._metadata.section_header = header
        return self
    
    def from_pdf_page(self, page: int) -> 'DocumentChunkBuilder':
        """Configure as a PDF page chunk."""
        self._metadata.file_type = FileType.PDF
        self._metadata.page_number = page
        return self
    
    def build(self) -> DocumentChunk:
        """Build the DocumentChunk."""
        return DocumentChunk(
            id=self._id,
            content=self._content,
            metadata=self._metadata
        )
