"""
Tests for the DocumentTitleExtractor class.
"""

from pathlib import Path

import pytest

from ...utils import DocumentTitleExtractor


class TestDocumentTitleExtractor:
    """Test cases for DocumentTitleExtractor."""

    @pytest.fixture
    def extractor(self):
        """Create a DocumentTitleExtractor instance."""
        return DocumentTitleExtractor()

    def test_extract_markdown_title_with_h1(self, extractor):
        """Test extracting title from Markdown with H1 header."""
        content = """# Introduction to AI

This is some content about AI.
"""
        file_path = Path("test.md")
        title = extractor.extract_title(file_path, content)
        assert title == "Introduction to AI"

    def test_extract_markdown_title_with_underline(self, extractor):
        """Test extracting title from Markdown with underlined header."""
        content = """Introduction to AI
==================

This is some content about AI.
"""
        file_path = Path("test.md")
        title = extractor.extract_title(file_path, content)
        assert title == "Introduction to AI"

    def test_extract_markdown_title_fallback_to_filename(self, extractor):
        """Test fallback to filename when no header found."""
        content = """This is just some content without headers."""
        file_path = Path("machine_learning_basics.md")
        title = extractor.extract_title(file_path, content)
        assert title == "Machine Learning Basics"

    def test_extract_pdf_title_from_content(self, extractor):
        """Test extracting title from PDF content."""
        content = """--- Page 1 ---
ARTIFICIAL INTELLIGENCE: A MODERN APPROACH

This is the content of the document.
"""
        file_path = Path("test.pd")
        title = extractor.extract_title(file_path, content)
        assert title == "ARTIFICIAL INTELLIGENCE: A MODERN APPROACH"

    def test_extract_pdf_title_fallback_to_filename(self, extractor):
        """Test PDF title extraction fallback to filename."""
        content = """--- Page 1 ---
This is just regular content without a clear title.
It continues with more text that doesn't look like a title.
"""
        file_path = Path("ai_research_paper.pd")
        title = extractor.extract_title(file_path, content)
        assert title == "Ai Research Paper"

    def test_extract_text_title_from_first_line(self, extractor):
        """Test extracting title from first substantial line of text."""
        content = """Natural Language Processing Overview

This document covers the basics of NLP.
"""
        file_path = Path("test.txt")
        title = extractor.extract_title(file_path, content)
        assert title == "Natural Language Processing Overview"

    def test_extract_text_title_fallback_to_filename(self, extractor):
        """Test text title extraction fallback to filename."""
        content = """Short.

More content that doesn't qualify as a title.
"""
        file_path = Path("deep_learning_notes.txt")
        title = extractor.extract_title(file_path, content)
        assert title == "Deep Learning Notes"

    def test_filename_to_title_conversion(self, extractor):
        """Test filename to title conversion."""
        file_path = Path("machine - learning_and_ai - basics.md")
        title = extractor._filename_to_title(file_path)
        assert title == "Machine Learning And Ai Basics"

    def test_extract_title_unknown_file_type(self, extractor):
        """Test title extraction for unknown file type."""
        content = """Some Title Here

Content follows.
"""
        file_path = Path("test.unknown")
        title = extractor.extract_title(file_path, content)
        assert title == "Some Title Here"
