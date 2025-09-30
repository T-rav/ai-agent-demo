"""
Tests for the ParagraphSplitter class.
"""

import pytest

from ...utils import ParagraphSplitter


class TestParagraphSplitter:
    """Test cases for ParagraphSplitter."""

    @pytest.fixture
    def splitter(self):
        """Create a ParagraphSplitter instance."""
        return ParagraphSplitter()

    def test_basic_paragraph_splitting(self, splitter):
        """Test basic paragraph splitting."""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        result = splitter.split(text)
        expected = ["First paragraph.", "Second paragraph.", "Third paragraph."]
        assert result == expected

    def test_paragraph_with_extra_whitespace(self, splitter):
        """Test paragraph splitting with extra whitespace."""
        text = "First paragraph.\n\n\n\nSecond paragraph with extra newlines.\n\n\nThird paragraph."
        result = splitter.split(text)
        expected = ["First paragraph.", "Second paragraph with extra newlines.", "Third paragraph."]
        assert result == expected

    def test_empty_text(self, splitter):
        """Test splitting empty text."""
        result = splitter.split("")
        assert result == []
