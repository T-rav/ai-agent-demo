"""
Token encoding service using tiktoken.
Implements the Single Responsibility Principle.
"""

from typing import List

try:
    import tiktoken
except ImportError:
    tiktoken = None

from ..models import ProcessingError


class TiktokenEncoder:
    """
    Token encoder using tiktoken library.

    Implements the TokenEncoder protocol.
    """

    def __init__(self, encoding_model: str = "cl100k_base") -> None:
        """
        Initialize the token encoder.

        Args:
            encoding_model: The tiktoken encoding model to use

        Raises:
            ProcessingError: If tiktoken is not available
        """
        if tiktoken is None:
            raise ProcessingError("tiktoken is required for token encoding")

        try:
            self._encoding = tiktoken.get_encoding(encoding_model)
        except Exception as e:
            raise ProcessingError("Failed to initialize tiktoken encoder: {e}") from e

    def encode(self, text: str) -> List[int]:
        """
        Encode text to tokens.

        Args:
            text: Text to encode

        Returns:
            List of token IDs
        """
        return self._encoding.encode(text)

    def decode(self, tokens: List[int]) -> str:
        """
        Decode tokens to text.

        Args:
            tokens: List of token IDs

        Returns:
            Decoded text
        """
        return self._encoding.decode(tokens)

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encode(text))
