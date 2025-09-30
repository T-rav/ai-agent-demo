"""
Document processing utilities for the ingestion pipeline.
Handles various file formats including PDF, Markdown, and text files.
Enhanced with semantic chunking and document structure awareness.
"""

import re
from pathlib import Path
from typing import Any, Dict, List

import PyPDF2
import tiktoken


class DocumentProcessor:
    """Processes various document formats and extracts text content."""

    def __init__(self, encoding_model: str = "cl100k_base"):
        """Initialize the document processor with tiktoken encoding."""
        self.encoding = tiktoken.get_encoding(encoding_model)

    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Process a single file and extract its content with enhanced metadata.

        Args:
            file_path: Path to the file to process

        Returns:
            Dictionary containing file metadata, content, and extracted title
        """
        try:
            content = self._extract_content(file_path)
            title = self._extract_title(file_path, content)

            return {
                "file_path": str(file_path),
                "file_name": file_path.name,
                "file_type": file_path.suffix.lower(),
                "title": title,
                "content": content,
                "token_count": len(self.encoding.encode(content)),
                "char_count": len(content),
            }
        except Exception:
            print("Error processing {file_path}: {str(e)}")
            return None

    def _extract_title(self, file_path: Path, content: str) -> str:
        """
        Extract document title from various sources.

        Args:
            file_path: Path to the document
            content: Document content

        Returns:
            Extracted or inferred document title
        """
        file_type = file_path.suffix.lower()

        if file_type == ".md":
            return self._extract_markdown_title(content, file_path)
        elif file_type == ".pd":
            return self._extract_pdf_title(content, file_path)
        else:
            return self._extract_text_title(content, file_path)

    def _extract_markdown_title(self, content: str, file_path: Path) -> str:
        """Extract title from Markdown content."""
        lines = content.split("\n")

        # Look for H1 headers (# Title)
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line.startswith("# ") and len(line) > 2:
                return line[2:].strip()

        # Look for underlined titles (Title\n===)
        for i, line in enumerate(lines[:10]):
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("==="):
                return line.strip()

        # Fallback to filename
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    def _extract_pdf_title(self, content: str, file_path: Path) -> str:
        """Extract title from PDF content."""
        lines = content.split("\n")

        # Look for title - like patterns in first few lines
        for line in lines[:20]:
            line = line.strip()
            if line and len(line) > 10 and len(line) < 200:
                # Skip page markers
                if line.startswith("--- Page"):
                    continue
                # Look for title - case or all - caps patterns
                if (line.istitle() or line.isupper()) and not line.endswith("."):
                    return line

        # Fallback to filename
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    def _extract_text_title(self, content: str, file_path: Path) -> str:
        """Extract title from plain text content."""
        lines = content.split("\n")

        # Look for first substantial line that could be a title
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) > 5 and len(line) < 200 and not line.endswith("."):
                return line

        # Fallback to filename
        return file_path.stem.replace("_", " ").replace("-", " ").title()

    def _extract_content(self, file_path: Path) -> str:
        """Extract text content based on file type."""
        file_type = file_path.suffix.lower()

        if file_type == ".pd":
            return self._extract_pdf_content(file_path)
        elif file_type in [".md", ".txt"]:
            return self._extract_text_content(file_path)
        else:
            # Try to read as text file
            return self._extract_text_content(file_path)

    def _extract_pdf_content(self, file_path: Path) -> str:
        """Extract text content from PDF files."""
        content = []

        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        content.append("--- Page {page_num + 1} ---\n{page_text}")
                except Exception:
                    print("Error extracting page {page_num + 1} from {file_path}: {str(e)}")

        return "\n\n".join(content)

    def _extract_text_content(self, file_path: Path) -> str:
        """Extract content from text - based files."""
        try:
            with open(file_path, "r", encoding="utf - 8") as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, "r", encoding="latin - 1") as file:
                return file.read()

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = re.sub(r"\n\s*\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text)

        # Remove special characters that might cause issues
        text = text.replace("\x00", "")

        return text.strip()


class SmartTextChunker:
    """
    Advanced text chunker with semantic and structure awareness.
    Handles different document types with appropriate chunking strategies.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        encoding_model: str = "cl100k_base",
        min_chunk_size: int = 100,
        max_chunk_size: int = 2000,
    ):
        """
        Initialize the smart text chunker.

        Args:
            chunk_size: Target tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
            encoding_model: Tiktoken encoding model to use
            min_chunk_size: Minimum chunk size in tokens
            max_chunk_size: Maximum chunk size in tokens
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.encoding = tiktoken.get_encoding(encoding_model)

    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a document into chunks using smart, structure - aware strategies.

        Args:
            document: Document dictionary with content and metadata

        Returns:
            List of chunk dictionaries with enhanced metadata
        """
        content = document.get("content", "")
        if not content:
            return []

        file_type = document.get("file_type", "").lower()

        # Choose chunking strategy based on document type
        if file_type == ".md":
            return self._chunk_markdown(document)
        elif file_type == ".pd":
            return self._chunk_pdf(document)
        else:
            return self._chunk_text(document)

    def _chunk_markdown(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk Markdown documents respecting structure."""
        content = document.get("content", "")
        chunks = []

        # Split by headers first
        sections = self._split_markdown_sections(content)

        for section in sections:
            section_chunks = self._chunk_section(document, section)
            chunks.extend(section_chunks)

        return chunks

    def _chunk_pdf(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk PDF documents with page awareness."""
        content = document.get("content", "")
        chunks = []

        # Split by pages first
        pages = content.split("--- Page ")

        for i, page_content in enumerate(pages):
            if not page_content.strip():
                continue

            # Add page number back for context
            if i > 0:
                page_content = "--- Page {page_content}"

            page_chunks = self._chunk_text_content(document, page_content, page_num=i if i > 0 else None)
            chunks.extend(page_chunks)

        return chunks

    def _chunk_text(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk plain text documents."""
        content = document.get("content", "")
        return self._chunk_text_content(document, content)

    def _split_markdown_sections(self, content: str) -> List[Dict[str, str]]:
        """Split Markdown content into sections based on headers."""
        lines = content.split("\n")
        sections = []
        current_section = {"header": "", "content": "", "level": 0}

        for line in lines:
            # Check for headers
            if line.strip().startswith("#"):
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)

                # Start new section
                header_level = len(line) - len(line.lstrip("#"))
                header_text = line.strip("#").strip()
                current_section = {"header": header_text, "content": line + "\n", "level": header_level}
            else:
                current_section["content"] += line + "\n"

        # Add final section
        if current_section["content"].strip():
            sections.append(current_section)

        return sections

    def _chunk_section(self, document: Dict[str, Any], section: Dict[str, str]) -> List[Dict[str, Any]]:
        """Chunk a document section intelligently."""
        content = section["content"]
        header = section.get("header", "")

        # If section is small enough, keep as single chunk
        token_count = len(self.encoding.encode(content))
        if token_count <= self.chunk_size:
            return [self._create_chunk(document, content, 0, section_header=header)]

        # Otherwise, chunk the content
        return self._chunk_text_content(document, content, section_header=header)

    def _chunk_text_content(
        self, document: Dict[str, Any], content: str, section_header: str = None, page_num: int = None
    ) -> List[Dict[str, Any]]:
        """Chunk text content with semantic awareness."""
        # Split into paragraphs first (better than sentences for most content)
        paragraphs = self._split_into_paragraphs(content)
        chunks = []
        current_chunk = []
        current_tokens = 0

        for paragraph in paragraphs:
            paragraph_tokens = len(self.encoding.encode(paragraph))

            # If single paragraph is too large, split it further
            if paragraph_tokens > self.max_chunk_size:
                # Split large paragraph by sentences
                sentences = self._split_into_sentences(paragraph)
                for sentence in sentences:
                    sentence_tokens = len(self.encoding.encode(sentence))

                    if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                        chunk_text = "\n\n".join(current_chunk)
                        chunks.append(
                            self._create_chunk(
                                document, chunk_text, len(chunks), section_header=section_header, page_num=page_num
                            )
                        )

                        # Start new chunk with overlap
                        overlap_text = self._get_overlap_text(chunk_text)
                        current_chunk = [overlap_text] if overlap_text else []
                        current_tokens = len(self.encoding.encode("\n\n".join(current_chunk)))

                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
            else:
                # Normal paragraph processing
                if current_tokens + paragraph_tokens > self.chunk_size and current_chunk:
                    chunk_text = "\n\n".join(current_chunk)
                    chunks.append(
                        self._create_chunk(
                            document, chunk_text, len(chunks), section_header=section_header, page_num=page_num
                        )
                    )

                    # Start new chunk with overlap
                    overlap_text = self._get_overlap_text(chunk_text)
                    current_chunk = [overlap_text] if overlap_text else []
                    current_tokens = len(self.encoding.encode("\n\n".join(current_chunk)))

                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens

        # Add final chunk if there's content
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            if len(self.encoding.encode(chunk_text)) >= self.min_chunk_size:
                chunks.append(
                    self._create_chunk(
                        document, chunk_text, len(chunks), section_header=section_header, page_num=page_num
                    )
                )

        return chunks

    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs for better chunk boundaries."""
        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in paragraphs if p.strip()]

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for better chunk boundaries."""
        # Enhanced sentence splitting with better patterns
        # Handle common abbreviations and edge cases
        text = re.sub(
            r"\b(?:Dr|Mr|Mrs|Ms|Prof|Sr|Jr|vs|etc|i\.e|e\.g)\.\s*", lambda m: m.group().replace(".", "<!DOT!>"), text
        )

        # Split on sentence endings
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Restore dots in abbreviations
        sentences = [s.replace("<!DOT!>", ".").strip() for s in sentences if s.strip()]

        return sentences

    def _get_overlap_text(self, chunk_text: str) -> str:
        """Get overlap text from the end of a chunk."""
        tokens = self.encoding.encode(chunk_text)
        if len(tokens) <= self.chunk_overlap:
            return chunk_text

        overlap_tokens = tokens[-self.chunk_overlap :]
        return self.encoding.decode(overlap_tokens)

    def _create_chunk(
        self,
        document: Dict[str, Any],
        chunk_text: str,
        chunk_index: int,
        section_header: str = None,
        page_num: int = None,
    ) -> Dict[str, Any]:
        """Create a chunk dictionary with enhanced metadata."""
        # Create unique chunk ID
        chunk_id = "{document['file_name']}_{chunk_index}"
        if section_header:
            # Clean section header for ID
            clean_header = re.sub(r"[^\w\s-]", "", section_header).strip()
            clean_header = re.sub(r"\s+", "_", clean_header)[:50]  # Limit length
            chunk_id = "{document['file_name']}_{clean_header}_{chunk_index}"

        metadata = {
            "file_path": document.get("file_path", ""),
            "file_name": document.get("file_name", ""),
            "file_type": document.get("file_type", ""),
            "document_title": document.get("title", ""),
            "chunk_index": chunk_index,
            "token_count": len(self.encoding.encode(chunk_text)),
            "char_count": len(chunk_text),
        }

        # Add section information if available
        if section_header:
            metadata["section_header"] = section_header

        # Add page information if available
        if page_num is not None:
            metadata["page_number"] = page_num

        return {"id": chunk_id, "content": chunk_text, "metadata": metadata}


# Backward compatibility alias
TextChunker = SmartTextChunker
