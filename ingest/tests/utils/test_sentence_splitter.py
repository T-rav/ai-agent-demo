"""
Tests for the SentenceSplitter class.
"""

import pytest

from ...utils import SentenceSplitter


class TestSentenceSplitter:
    """Test cases for SentenceSplitter."""

    @pytest.fixture
    def splitter(self):
        """Create a SentenceSplitter instance."""
        return SentenceSplitter()

    def test_basic_sentence_splitting(self, splitter):
        """Test basic sentence splitting."""
        text = "This is the first sentence. This is the second sentence! Is this the third?"
        result = splitter.split(text)
        expected = ["This is the first sentence.", "This is the second sentence!", "Is this the third?"]
        assert result == expected

    def test_abbreviation_handling(self, splitter):
        """Test that abbreviations don't cause incorrect splits."""
        text = "Dr. Smith went to the U.S.A. He had a great time."
        result = splitter.split(text)
        expected = ["Dr. Smith went to the U.S.A.", "He had a great time."]
        assert result == expected

    def test_empty_text(self, splitter):
        """Test splitting empty text."""
        result = splitter.split("")
        assert result == []

    def test_single_sentence(self, splitter):
        """Test splitting text with only one sentence."""
        text = "This is a single sentence."
        result = splitter.split(text)
        assert result == ["This is a single sentence."]
