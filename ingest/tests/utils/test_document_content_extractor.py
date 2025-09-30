"""
Tests for the content extraction utilities.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from ...utils import DocumentContentExtractor
from ...models import ProcessingError


class TestDocumentContentExtractor:
    """Test cases for DocumentContentExtractor."""
    
    @pytest.fixture
    def extractor(self):
        """Create a DocumentContentExtractor instance."""
        return DocumentContentExtractor()
    
    def test_extract_markdown_content(self, extractor):
        """Test extracting content from Markdown files."""
        md_path = Path("/test/sample.md")
        md_content = "# Title\n\nThis is markdown content."
        
        with patch('builtins.open', mock_open(read_data=md_content)):
            result = extractor.extract_content(md_path)
            
            assert result == md_content
    
    def test_extract_text_content(self, extractor):
        """Test extracting content from text files."""
        txt_path = Path("/test/sample.txt")
        txt_content = "This is plain text content."
        
        with patch('builtins.open', mock_open(read_data=txt_content)):
            result = extractor.extract_content(txt_path)
            
            assert result == txt_content
    
    @patch('ingest.utils.content_extractor.PyPDF2')
    def test_extract_pdf_content_success(self, mock_pypdf2, extractor):
        """Test successful PDF content extraction."""
        pdf_path = Path("/test/sample.pdf")
        
        # Mock PyPDF2 objects
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "--- Page 1 ---\nPDF page content"
        
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "\n--- Page 2 ---\nPDF page content"
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2]
        
        mock_pypdf2.PdfReader.return_value = mock_reader
        
        with patch('builtins.open', mock_open()):
            result = extractor.extract_content(pdf_path)
            
            # The actual implementation includes page markers
            assert "--- Page 1 ---" in result
            assert "--- Page 2 ---" in result
            assert "PDF page content" in result
    
    def test_extract_pdf_content_pypdf2_not_available(self, extractor):
        """Test PDF extraction when PyPDF2 is not available."""
        pdf_path = Path("/test/sample.pdf")
        
        # Set PyPDF2 to None to simulate import failure
        with patch('ingest.utils.content_extractor.PyPDF2', None):
            with pytest.raises(ProcessingError, match="PyPDF2 is required for PDF processing"):
                extractor.extract_content(pdf_path)
    
    @patch('ingest.utils.content_extractor.PyPDF2')
    def test_extract_pdf_content_error(self, mock_pypdf2, extractor):
        """Test PDF extraction error handling."""
        pdf_path = Path("/test/sample.pdf")
        
        mock_pypdf2.PdfReader.side_effect = Exception("PDF read error")
        
        with patch('builtins.open', mock_open()):
            with pytest.raises(ProcessingError, match="Failed to read PDF file"):
                extractor.extract_content(pdf_path)
    
    def test_extract_unsupported_file_type(self, extractor):
        """Test extracting content from unsupported file types."""
        docx_path = Path("/test/sample.docx")
        
        with pytest.raises(ProcessingError, match="Failed to extract content"):
            extractor.extract_content(docx_path)
    
    def test_extract_content_file_not_found(self, extractor):
        """Test handling file not found errors."""
        missing_path = Path("/test/missing.txt")
        
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            with pytest.raises(ProcessingError, match="Failed to extract content"):
                extractor.extract_content(missing_path)
    
    def test_extract_content_permission_error(self, extractor):
        """Test handling permission errors."""
        restricted_path = Path("/test/restricted.txt")
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(ProcessingError, match="Failed to extract content"):
                extractor.extract_content(restricted_path)


