"""
Content extraction service for various document formats.
Implements the Single Responsibility Principle.
"""

import re
from pathlib import Path
from typing import Callable, Dict

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

from ..models import ProcessingError


class DocumentContentExtractor:
    """
    Extracts text content from various file formats.

    Follows the Strategy pattern for different extraction methods.
    """

    def __init__(self) -> None:
        """Initialize the content extractor with format strategies."""
        self._extractors: Dict[str, Callable[[Path], str]] = {
            ".pdf": self._extract_pdf_content,
            ".md": self._extract_text_content,
            ".txt": self._extract_text_content,
        }

    def extract_content(self, file_path: Path) -> str:
        """
        Extract text content from a file based on its type.

        Args:
            file_path: Path to the file

        Returns:
            Extracted text content

        Raises:
            ProcessingError: If content extraction fails
        """
        file_type = file_path.suffix.lower()
        extractor = self._extractors.get(file_type, self._extract_text_content)

        try:
            return extractor(file_path)
        except Exception as e:
            raise ProcessingError(f"Failed to extract content from {file_path}: {e}") from e

    def _extract_pdf_content(self, file_path: Path) -> str:
        """Extract text content from PDF files."""
        if PyPDF2 is None:
            raise ProcessingError("PyPDF2 is required for PDF processing")

        content = []

        try:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            content.append(f"--- Page {page_num + 1} ---\n{page_text}")
                    except Exception as page_error:
                        msg = f"Warning: Error extracting page {page_num + 1} from {file_path}"
                        print(f"{msg}: {page_error}")
        except Exception as e:
            raise ProcessingError(f"Failed to read PDF file {file_path}: {e}") from e

        return "\n\n".join(content)

    def _extract_text_content(self, file_path: Path) -> str:
        """Extract content from text - based files."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, "r", encoding="latin-1") as file:
                    return file.read()
            except Exception as e:
                raise ProcessingError(f"Failed to read text file {file_path}: {e}") from e
        except Exception as e:
            raise ProcessingError(f"Failed to read file {file_path}: {e}") from e


class TextCleaner:
    """
    Cleans and normalizes text content.

    Follows the Single Responsibility Principle.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text content.

        Args:
            text: Raw text content

        Returns:
            Cleaned text content
        """
        # Remove excessive whitespace
        text = re.sub(r"\n\s*\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text)

        # Remove special characters that might cause issues
        text = text.replace("\x00", "")

        return text.strip()
