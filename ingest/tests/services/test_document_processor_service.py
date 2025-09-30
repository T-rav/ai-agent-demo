"""
Tests for the DocumentProcessorService class.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from ...models import FileType, ProcessedDocument, ProcessingError
from ...services import DocumentProcessorService


class TestDocumentProcessorService:
    """Test cases for DocumentProcessorService."""

    @pytest.fixture
    def service(self):
        """Create a DocumentProcessorService instance."""
        return DocumentProcessorService()

    @pytest.fixture
    def mock_file_path(self):
        """Create a mock file path."""
        return Path("/test / sample.md")

    def test_process_markdown_file(self, service, mock_file_path):
        """Test processing a Markdown file."""
        mock_content = "# Test Document\n\nThis is test content."

        with patch.object(service._content_extractor, "extract_content", return_value=mock_content):
            with patch.object(service._title_extractor, "extract_title", return_value="Test Document"):
                with patch.object(service._text_cleaner, "clean_text", return_value=mock_content):
                    with patch.object(service._token_encoder, "count_tokens", return_value=10):

                        result = service.process_file(mock_file_path)

                        assert isinstance(result, ProcessedDocument)
                        assert result.file_path == str(mock_file_path)
                        assert result.file_name == "sample.md"
                        assert result.file_type == FileType.MARKDOWN
                        assert result.title == "Test Document"
                        assert result.content == mock_content
                        assert result.token_count == 10
                        assert result.char_count == len(mock_content)

    def test_process_pdf_file(self, service):
        """Test processing a PDF file."""
        pdf_path = Path("/test / sample.pd")
        mock_content = "PDF content here"

        with patch.object(service._content_extractor, "extract_content", return_value=mock_content):
            with patch.object(service._title_extractor, "extract_title", return_value="PDF Title"):
                with patch.object(service._text_cleaner, "clean_text", return_value=mock_content):
                    with patch.object(service._token_encoder, "count_tokens", return_value=5):

                        result = service.process_file(pdf_path)

                        assert result.file_type == FileType.PDF
                        assert result.title == "PDF Title"

    def test_process_text_file(self, service):
        """Test processing a text file."""
        txt_path = Path("/test / sample.txt")
        mock_content = "Plain text content"

        with patch.object(service._content_extractor, "extract_content", return_value=mock_content):
            with patch.object(service._title_extractor, "extract_title", return_value="Text Title"):
                with patch.object(service._text_cleaner, "clean_text", return_value=mock_content):
                    with patch.object(service._token_encoder, "count_tokens", return_value=3):

                        result = service.process_file(txt_path)

                        assert result.file_type == FileType.TEXT
                        assert result.title == "Text Title"

    def test_process_unsupported_file_type(self, service):
        """Test processing an unsupported file type."""
        unsupported_path = Path("/test / sample.docx")

        result = service.process_file(unsupported_path)

        assert result is None

    def test_process_file_content_extraction_error(self, service, mock_file_path):
        """Test handling content extraction errors."""
        with patch.object(
            service._content_extractor, "extract_content", side_effect=ProcessingError("Extraction failed")
        ):

            result = service.process_file(mock_file_path)

            assert result is None

    def test_process_file_empty_content(self, service, mock_file_path):
        """Test processing file with empty content."""
        with patch.object(service._content_extractor, "extract_content", return_value=""):

            result = service.process_file(mock_file_path)

            assert result is None

    def test_process_file_whitespace_only_content(self, service, mock_file_path):
        """Test processing file with whitespace - only content."""
        with patch.object(service._content_extractor, "extract_content", return_value="   \n\t  "):
            with patch.object(service._text_cleaner, "clean_text", return_value=""):

                result = service.process_file(mock_file_path)

                assert result is None

    # Note: The DocumentProcessorService doesn't expose file type detection methods
    # as they are handled internally. These tests would be better suited for
    # integration tests or testing the internal logic through the main process_file method.
