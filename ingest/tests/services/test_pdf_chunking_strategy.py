"""
Tests for the PDFChunkingStrategy class.
"""

import pytest
from unittest.mock import Mock

from ...services.chunking_service import PDFChunkingStrategy
from ...services import DocumentChunkingService
from ...models import ProcessedDocument, FileType


class TestPDFChunkingStrategy:
    """Test cases for PDFChunkingStrategy."""
    
    @pytest.fixture
    def mock_token_encoder(self):
        """Create a mock token encoder."""
        encoder = Mock()
        encoder.count_tokens.side_effect = lambda text: len(text.split())
        return encoder
    
    @pytest.fixture
    def sample_pdf_content(self):
        """Sample PDF content for testing."""
        return """--- Page 1 ---
ARTIFICIAL INTELLIGENCE: A COMPREHENSIVE GUIDE

This document provides a comprehensive overview of artificial intelligence.

--- Page 2 ---
INTRODUCTION

Artificial Intelligence (AI) is a rapidly growing field in computer science.

--- Page 3 ---
MACHINE LEARNING

Machine learning is a subset of AI that focuses on algorithms
that can learn and improve from experience."""
    
    def test_pdf_chunking_strategy(self, mock_token_encoder, sample_pdf_content):
        """Test PDF chunking strategy."""
        strategy = PDFChunkingStrategy()
        chunking_service = DocumentChunkingService(
            token_encoder=mock_token_encoder,
            chunk_size=50,  # Small chunk size to ensure chunking happens
            chunk_overlap=10,
            min_chunk_size=10,
            max_chunk_size=100
        )
        
        document = ProcessedDocument(
            file_path="/test/sample.pdf",
            file_name="sample.pdf",
            file_type=FileType.PDF,
            title="AI Guide",
            content=sample_pdf_content,
            token_count=100,
            char_count=len(sample_pdf_content)
        )
        
        chunks = strategy.chunk(document, chunking_service)
        assert len(chunks) > 0
        
        # Check that chunks have proper metadata
        for chunk in chunks:
            assert chunk.metadata.file_type == FileType.PDF
            assert chunk.metadata.document_title == "AI Guide"
