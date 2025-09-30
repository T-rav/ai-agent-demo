"""
Factory for creating sample content and content - related test doubles.
"""

from pathlib import Path
from unittest.mock import Mock


class ContentFactory:
    """Factory methods for creating sample content."""

    @staticmethod
    def create_sample_markdown_content() -> str:
        """Create sample markdown content for testing."""
        return """# Introduction to AI

This is an introduction to artificial intelligence.

## Machine Learning

Machine learning is a subset of AI that focuses on algorithms.

### Supervised Learning

Supervised learning uses labeled data to train models.

## Deep Learning

Deep learning uses neural networks with multiple layers.
"""

    @staticmethod
    def create_sample_pdf_content() -> str:
        """Create sample PDF content for testing."""
        return """--- Page 1 ---
Artificial Intelligence Research Paper

Abstract: This paper discusses the latest advances in AI.

Introduction: AI has become increasingly important in modern technology.

--- Page 2 ---
Methodology: We used machine learning algorithms to analyze data.

Results: Our experiments show significant improvements in accuracy.

Conclusion: AI continues to evolve and improve.
"""

    @staticmethod
    def create_sample_text_content() -> str:
        """Create sample text content for testing."""
        return """Natural Language Processing Guide

Natural language processing (NLP) is a field of artificial intelligence.

It focuses on the interaction between computers and human language.

Key applications include:
- Text analysis
- Machine translation
- Sentiment analysis
- Chatbots and virtual assistants

NLP combines computational linguistics with machine learning.
"""

    @staticmethod
    def create_test_file_path(filename: str = "test_document.md") -> Path:
        """Create a test file path."""
        return Path("/test / path/{filename}")

    @staticmethod
    def create_mock_content_extractor() -> Mock:
        """Create a mock content extractor."""
        extractor = Mock()
        extractor.extract_content.return_value = "Sample extracted content"
        return extractor

    @staticmethod
    def create_mock_title_extractor() -> Mock:
        """Create a mock title extractor."""
        extractor = Mock()
        extractor.extract_title.return_value = "Sample Title"
        return extractor

    @staticmethod
    def create_mock_text_cleaner() -> Mock:
        """Create a mock text cleaner."""
        cleaner = Mock()
        cleaner.clean_text.side_effect = lambda text: text.strip()
        return cleaner
