"""
Factory for creating token encoder test doubles.
"""

from unittest.mock import Mock


class MockTokenEncoder:
    """Mock token encoder implementation for testing."""

    def encode(self, text: str) -> list[int]:
        # Rough approximation: 1 token per 4 characters
        return list(range(len(text) // 4))

    def decode(self, tokens: list[int]) -> str:
        return "mock_decoded_text"

    def count_tokens(self, text: str) -> int:
        return len(text) // 4


class TokenFactory:
    """Factory methods for creating token encoder test doubles."""

    @staticmethod
    def create_mock_token_encoder() -> Mock:
        """Create a properly configured mock token encoder."""
        encoder = Mock()
        encoder.count_tokens.side_effect = lambda text: len(text.split()) if text else 0
        encoder.encode.side_effect = lambda text: list(range(len(text.split()))) if text else []
        encoder.decode.side_effect = (
            lambda tokens: " ".join([f"token{i}" for i in tokens]) if tokens else ""
        )
        return encoder

    @staticmethod
    def create_simple_mock_token_encoder() -> MockTokenEncoder:
        """Create a simple mock token encoder implementation."""
        return MockTokenEncoder()
