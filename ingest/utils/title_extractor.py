"""
Title extraction service for various document formats.
Implements the Single Responsibility Principle.
"""

from pathlib import Path
from typing import Callable, Dict

# No imports needed for this standalone class


class DocumentTitleExtractor:
    """
    Extracts document titles from various file formats.

    Follows the Strategy pattern for different extraction methods.
    """

    def __init__(self) -> None:
        """Initialize the title extractor with format strategies."""
        self._extractors: Dict[str, Callable[[str, Path], str]] = {
            ".md": self._extract_markdown_title,
            ".pdf": self._extract_pdf_title,
            ".txt": self._extract_text_title,
        }

    def extract_title(self, file_path: Path, content: str) -> str:
        """
        Extract document title from content based on file type.

        Args:
            file_path: Path to the document
            content: Document content

        Returns:
            Extracted or inferred document title
        """
        file_type = file_path.suffix.lower()
        extractor = self._extractors.get(file_type, self._extract_text_title)
        return extractor(content, file_path)

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
        return self._filename_to_title(file_path)

    def _extract_pdf_title(self, content: str, file_path: Path) -> str:
        """Extract title from PDF content."""
        lines = content.split("\n")

        # Look for title - like patterns in first few lines
        for line in lines[:20]:
            line = line.strip()
            if line and 10 < len(line) < 200:
                # Skip page markers
                if line.startswith("--- Page"):
                    continue
                # Look for title - case or all - caps patterns
                if (line.istitle() or line.isupper()) and not line.endswith("."):
                    return line

        # Fallback to filename
        return self._filename_to_title(file_path)

    def _extract_text_title(self, content: str, file_path: Path) -> str:
        """Extract title from plain text content."""
        lines = content.split("\n")

        # Look for first substantial line that could be a title
        for line in lines[:5]:
            line = line.strip()
            if line and 5 < len(line) < 200 and not line.endswith("."):
                return line

        # Fallback to filename
        return self._filename_to_title(file_path)

    def _filename_to_title(self, file_path: Path) -> str:
        """Convert filename to a readable title."""
        return file_path.stem.replace("_", " ").replace("-", " ").title()
