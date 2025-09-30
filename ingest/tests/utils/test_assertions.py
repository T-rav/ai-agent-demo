"""
Custom assertion helpers for test validation.
"""

from typing import List


class TestAssertions:
    """Custom assertion helpers for test validation."""

    @staticmethod
    def assert_processed_document_valid(document, expected_title: str = None):
        """Assert that a ProcessedDocument is valid."""
        assert document is not None
        assert hasattr(document, "file_path")
        assert hasattr(document, "file_type")
        assert hasattr(document, "title")
        assert hasattr(document, "content")
        assert hasattr(document, "token_count")
        assert hasattr(document, "char_count")

        if expected_title:
            assert document.title == expected_title

        assert document.token_count >= 0
        assert document.char_count >= 0

    @staticmethod
    def assert_document_chunk_valid(chunk, expected_content: str = None):
        """Assert that a DocumentChunk is valid."""
        assert chunk is not None
        assert hasattr(chunk, "id")
        assert hasattr(chunk, "content")
        assert hasattr(chunk, "metadata")

        if expected_content:
            assert expected_content in chunk.content

        assert chunk.metadata.token_count >= 0
        assert chunk.metadata.char_count >= 0
        assert chunk.metadata.chunk_index >= 0

    @staticmethod
    def assert_ingestion_config_valid(config, expected_model: str = None):
        """Assert that an IngestionConfig is valid."""
        assert config is not None
        assert hasattr(config, "openai_api_key")
        assert hasattr(config, "pinecone_api_key")
        assert hasattr(config, "pinecone_environment")
        assert hasattr(config, "index_name")
        assert hasattr(config, "model")
        assert hasattr(config, "dimensions")

        if expected_model:
            assert config.model == expected_model

        assert config.dimensions > 0
        assert config.chunk_size > 0
        assert config.chunk_overlap >= 0

    @staticmethod
    def assert_chunks_have_proper_metadata(chunks: List, expected_title: str = None):
        """Assert that chunks have proper metadata."""
        assert len(chunks) > 0

        for i, chunk in enumerate(chunks):
            TestAssertions.assert_document_chunk_valid(chunk)
            assert chunk.metadata.chunk_index == i
            assert chunk.metadata is not None

            if expected_title:
                assert chunk.metadata.document_title == expected_title

    @staticmethod
    def assert_mock_called_with_content(mock_obj, expected_content: str):
        """Assert that a mock was called with specific content."""
        mock_obj.assert_called()
        call_args = mock_obj.call_args
        if call_args:
            args, kwargs = call_args
            content_found = any(expected_content in str(arg) for arg in args)
            content_found = content_found or any(expected_content in str(val) for val in kwargs.values())
            assert content_found, "Expected content '{expected_content}' not found in mock calls"
