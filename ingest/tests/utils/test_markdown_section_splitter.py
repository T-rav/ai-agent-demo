"""
Tests for the MarkdownSectionSplitter class.
"""

import pytest

from ...utils import MarkdownSectionSplitter


class TestMarkdownSectionSplitter:
    """Test cases for MarkdownSectionSplitter."""

    @pytest.fixture
    def splitter(self):
        """Create a MarkdownSectionSplitter instance."""
        return MarkdownSectionSplitter()

    def test_basic_section_splitting(self, splitter):
        """Test basic Markdown section splitting."""
        text = """# Introduction
This is the introduction.

## Background
This is the background section.

### Details
More detailed information here.

## Conclusion
Final thoughts."""

        result = splitter.split(text)
        # The actual implementation returns dictionaries with header, content, and level
        assert len(result) == 4
        assert all(isinstance(section, dict) for section in result)
        assert all("header" in section and "content" in section and "level" in section for section in result)

        # Check the first section
        assert result[0]["header"] == "Introduction"
        assert result[0]["level"] == 1
        assert "This is the introduction" in result[0]["content"]

    def test_content_without_headers(self, splitter):
        """Test content that doesn't start with headers."""
        text = """Some initial content without headers.

# First Header
Content under first header.

## Second Header
Content under second header."""

        result = splitter.split(text)
        # The actual implementation returns dictionaries
        assert len(result) >= 2  # At least the headers
        assert all(isinstance(section, dict) for section in result)

        # Check that we have the expected headers
        headers = [section["header"] for section in result if section.get("header")]
        assert "First Header" in headers
        assert "Second Header" in headers

    def test_empty_text(self, splitter):
        """Test splitting empty text."""
        result = splitter.split("")
        assert result == []
