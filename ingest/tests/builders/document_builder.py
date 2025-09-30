"""
Fluent builder for ProcessedDocument objects.
"""

from pathlib import Path
from typing import Any, Dict, Union

from ...models import FileType, ProcessedDocument


class ProcessedDocumentBuilder:
    """Fluent builder for ProcessedDocument objects."""

    def __init__(self):
        self._file_path = "/test / document.md"
        self._file_name = "document.md"
        self._file_type = FileType.MARKDOWN
        self._title = "Test Document"
        self._content = "Sample content for testing"
        self._token_count = 10
        self._char_count = 25
        self._metadata = {}

    def with_file_path(self, file_path: Union[str, Path]) -> "ProcessedDocumentBuilder":
        """Set the file path."""
        self._file_path = str(file_path)
        if isinstance(file_path, Path):
            self._file_name = file_path.name
        else:
            self._file_name = Path(file_path).name
        return self

    def with_file_type(self, file_type: FileType) -> "ProcessedDocumentBuilder":
        """Set the file type."""
        self._file_type = file_type
        return self

    def with_title(self, title: str) -> "ProcessedDocumentBuilder":
        """Set the document title."""
        self._title = title
        return self

    def with_content(self, content: str) -> "ProcessedDocumentBuilder":
        """Set the document content."""
        self._content = content
        return self

    def with_token_count(self, count: int) -> "ProcessedDocumentBuilder":
        """Set the token count."""
        self._token_count = count
        return self

    def with_char_count(self, count: int) -> "ProcessedDocumentBuilder":
        """Set the character count."""
        self._char_count = count
        return self

    def with_metadata(self, metadata: Dict[str, Any]) -> "ProcessedDocumentBuilder":
        """Set the metadata."""
        self._metadata = metadata
        return self

    def as_markdown(self) -> "ProcessedDocumentBuilder":
        """Configure as a markdown document."""
        return self.with_file_type(FileType.MARKDOWN).with_file_path("/test / document.md")

    def as_pdf(self) -> "ProcessedDocumentBuilder":
        """Configure as a PDF document."""
        return self.with_file_type(FileType.PDF).with_file_path("/test/document.pdf")

    def as_text(self) -> "ProcessedDocumentBuilder":
        """Configure as a text document."""
        return self.with_file_type(FileType.TEXT).with_file_path("/test / document.txt")

    def with_long_content(self) -> "ProcessedDocumentBuilder":
        """Set long content for chunking tests."""
        long_content = " ".join(["This is sentence {i} in a long document." for i in range(100)])
        return self.with_content(long_content).with_token_count(500).with_char_count(len(long_content))

    def with_empty_content(self) -> "ProcessedDocumentBuilder":
        """Set empty content."""
        return (
            self.with_content("Empty document content").with_token_count(3).with_char_count(20)
        )  # Pydantic requires non - empty string

    def build(self) -> ProcessedDocument:
        """Build the ProcessedDocument."""
        return ProcessedDocument(
            file_name=self._file_name,
            file_type=self._file_type,
            title=self._title,
            content=self._content,
            token_count=self._token_count,
            char_count=self._char_count,
        )
