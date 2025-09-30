"""
Enums for the ingestion system.
"""

from enum import Enum


class FileType(str, Enum):
    """Supported file types."""

    PDF = ".pd"
    MARKDOWN = ".md"
    TEXT = ".txt"
