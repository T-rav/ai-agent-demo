"""
Context manager for common mock scenarios.
"""

import os
from contextlib import contextmanager
from typing import Any, Dict
from unittest.mock import Mock, mock_open, patch


class MockContextManager:
    """Context manager for common mock scenarios."""

    @staticmethod
    @contextmanager
    def mock_file_operations(file_content: str = "", file_exists: bool = True):
        """Mock file operations with specified content and existence."""
        with patch("builtins.open", mock_open(read_data=file_content.encode())):
            with patch("pathlib.Path.exists", return_value=file_exists):
                yield

    @staticmethod
    @contextmanager
    def mock_config_loading(config_data: Dict[str, Any]):
        """Mock configuration loading with specified data."""
        mock_config = Mock()
        mock_config.validate_required_config.return_value = None
        mock_config.get_all_config.return_value = config_data

        with patch("ingest.core.config_loader.Config.__init__") as mock_init:
            mock_init.return_value = None
            with patch("ingest.core.config_loader.Config", return_value=mock_config):
                yield mock_config

    @staticmethod
    @contextmanager
    def mock_environment_variables(env_vars: Dict[str, str], clear: bool = False):
        """Mock environment variables."""
        with patch.dict(os.environ, env_vars, clear=clear):
            yield

    @staticmethod
    @contextmanager
    def mock_tiktoken():
        """Mock tiktoken library."""
        mock_encoding = Mock()
        mock_encoding.encode.return_value = [1, 2, 3, 4, 5]
        mock_encoding.decode.return_value = "decoded text"

        with patch("ingest.utils.token_encoder.tiktoken") as mock_tiktoken:
            mock_tiktoken.get_encoding.return_value = mock_encoding
            yield mock_tiktoken, mock_encoding

    @staticmethod
    @contextmanager
    def mock_pypdf2():
        """Mock PyPDF2 library."""
        mock_page = Mock()
        mock_page.extract_text.return_value = "--- Page 1 ---\nSample PDF content"

        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        with patch("ingest.utils.content_extractor.PyPDF2") as mock_pypdf2:
            mock_pypdf2.PdfReader.return_value = mock_reader
            yield mock_pypdf2, mock_reader, mock_page
