"""
Tests for the MarkdownChunkingStrategy class.
"""

from unittest.mock import Mock

import pytest

from ...models import FileType, ProcessedDocument
from ...services import DocumentChunkingService
from ...services.chunking_service import MarkdownChunkingStrategy


class TestMarkdownChunkingStrategy:
    """Test cases for MarkdownChunkingStrategy."""

    @pytest.fixture
    def mock_token_encoder(self):
        """Create a mock token encoder."""
        encoder = Mock()
        encoder.count_tokens.side_effect = lambda text: len(text.split())
        return encoder

    @pytest.fixture
    def sample_markdown_content(self):
        """Sample Markdown content for testing."""
        return """# Introduction to AI

This is the introduction section with some content about artificial intelligence.

## What is AI?

Artificial Intelligence (AI) refers to the simulation of human intelligence in machines.

### Machine Learning

Machine learning is a subset of AI that focuses on algorithms.

## Applications

AI has many applications in various fields including:

- Healthcare
- Finance
- Transportation
- Entertainment"""

    def test_markdown_chunking_strategy(self, mock_token_encoder, sample_markdown_content):
        """Test Markdown chunking strategy."""
        strategy = MarkdownChunkingStrategy()
        chunking_service = DocumentChunkingService(token_encoder=mock_token_encoder)

        document = ProcessedDocument(
            file_path="/test / sample.md",
            file_name="sample.md",
            file_type=FileType.MARKDOWN,
            title="AI Guide",
            content=sample_markdown_content,
            token_count=100,
            char_count=len(sample_markdown_content),
        )

        chunks = strategy.chunk(document, chunking_service)
        assert len(chunks) > 0

        # Check that chunks have proper metadata
        for chunk in chunks:
            assert chunk.metadata.file_type == FileType.MARKDOWN
            assert chunk.metadata.document_title == "AI Guide"
            assert chunk.metadata.section_header is not None  # Should extract headers
