"""
Text splitting utilities for document chunking.
Implements the Single Responsibility Principle.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


class TextSplitter(ABC):
    """Abstract base class for text splitting strategies."""

    @abstractmethod
    def split(self, text: str) -> Union[List[str], List[Dict[str, Any]]]:
        """Split text into segments."""


class SentenceSplitter(TextSplitter):
    """
    Splits text into sentences with improved handling of abbreviations.
    """

    def __init__(self) -> None:
        """Initialize the sentence splitter."""
        # Common abbreviations that shouldn't trigger sentence breaks
        self._abbreviations = {
            "Dr",
            "Mr",
            "Mrs",
            "Ms",
            "Prof",
            "Sr",
            "Jr",
            "vs",
            "etc",
            "i.e",
            "e.g",
            "Ph.D",
            "M.D",
            "B.A",
            "M.A",
            "Inc",
            "Corp",
            "Ltd",
            "Co",
            "St",
            "Ave",
            "Blvd",
        }

    def split(self, text: str) -> List[str]:
        """
        Split text into sentences with better handling of edge cases.

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        # Protect abbreviations by temporarily replacing dots
        protected_text = self._protect_abbreviations(text)

        # Split on sentence endings
        sentences = re.split(r"(?<=[.!?])\s+", protected_text)

        # Restore dots in abbreviations and clean up
        sentences = [self._restore_abbreviations(s).strip() for s in sentences if s.strip()]

        return sentences

    def _protect_abbreviations(self, text: str) -> str:
        """Replace dots in abbreviations with placeholder."""
        pattern = r"\b(?:" + "|".join(re.escape(abbr) for abbr in self._abbreviations) + r")\."
        return re.sub(pattern, lambda m: m.group().replace(".", "<!DOT!>"), text, flags=re.IGNORECASE)

    def _restore_abbreviations(self, text: str) -> str:
        """Restore dots in abbreviations."""
        return text.replace("<!DOT!>", ".")


class ParagraphSplitter(TextSplitter):
    """
    Splits text into paragraphs based on double newlines.
    """

    def split(self, text: str) -> List[str]:
        """
        Split text into paragraphs.

        Args:
            text: Text to split

        Returns:
            List of paragraphs
        """
        # Split by double newlines (paragraph breaks)
        paragraphs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in paragraphs if p.strip()]


class MarkdownSectionSplitter(TextSplitter):
    """
    Splits Markdown text into sections based on headers.
    """

    def split(self, text: str) -> List[Dict[str, Any]]:
        """
        Split Markdown text into sections.

        Args:
            text: Markdown text to split

        Returns:
            List of section dictionaries with header and content
        """
        lines = text.split("\n")
        sections = []
        current_section = {"header": "", "content": "", "level": 0}

        for line in lines:
            # Check for headers
            if line.strip().startswith("#"):
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)

                # Start new section
                header_level = len(line) - len(line.lstrip("#"))
                header_text = line.strip("#").strip()
                current_section = {"header": header_text, "content": line + "\n", "level": header_level}
            else:
                current_section["content"] += line + "\n"

        # Add final section
        if current_section["content"].strip():
            sections.append(current_section)

        return sections
