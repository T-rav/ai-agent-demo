"""
Tests for the TextChunkingStrategy class.
"""

from unittest.mock import Mock

import pytest

from ...models import FileType, ProcessedDocument
from ...services import DocumentChunkingService
from ...services.chunking_service import TextChunkingStrategy


class TestTextChunkingStrategy:
    """Test cases for TextChunkingStrategy."""

    @pytest.fixture
    def mock_token_encoder(self):
        """Create a mock token encoder."""
        encoder = Mock()
        encoder.count_tokens.side_effect = lambda text: len(text.split()) if text else 0
        encoder.encode.side_effect = lambda text: list(range(len(text.split()))) if text else []
        encoder.decode.side_effect = lambda tokens: " ".join([f"token{i}" for i in tokens]) if tokens else ""
        return encoder

    @pytest.fixture
    def sample_text_content(self):
        """Sample text content for testing."""
        return """Introduction to Natural Language Processing

Natural Language Processing (NLP) is a branch of artificial intelligence
that focuses on the interaction between computers and humans through natural language.

The goal of NLP is to enable computers to understand, interpret, and generate
human language in a way that is both meaningful and useful.

Applications of NLP include:
- Text analysis
- Machine translation
- Sentiment analysis
- Chatbots and virtual assistants"""

    def test_text_chunking_strategy(self, mock_token_encoder, sample_text_content):
        """Test text chunking strategy."""
        strategy = TextChunkingStrategy()
        chunking_service = DocumentChunkingService(
            token_encoder=mock_token_encoder,
            chunk_size=50,  # Small chunk size to ensure chunking happens
            chunk_overlap=10,
            min_chunk_size=10,
            max_chunk_size=100,
        )

        document = ProcessedDocument(
            file_name="sample.txt",
            file_type=FileType.TEXT,
            title="NLP Guide",
            content=sample_text_content,
            token_count=100,
            char_count=len(sample_text_content),
        )

        chunks = strategy.chunk(document, chunking_service)
        assert len(chunks) > 0

        # Check that chunks have proper metadata
        for chunk in chunks:
            assert chunk.metadata.file_type == FileType.TEXT
            assert chunk.metadata.document_title == "NLP Guide"
            # Text chunks typically don't have page numbers or section headers
            assert chunk.metadata.page_number is None
