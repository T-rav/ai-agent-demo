"""
Factory for creating LLM test doubles.
"""

from unittest.mock import AsyncMock

from langchain_core.messages import AIMessage


class LLMFactory:
    """Factory methods for creating LLM test doubles."""

    @staticmethod
    def create_mock_llm():
        """Create a mock LLM."""
        from unittest.mock import MagicMock

        mock = MagicMock()

        # Mock ainvoke
        mock.ainvoke = AsyncMock(
            return_value=AIMessage(content="This is a test response from the LLM.")
        )

        # Mock astream
        async def mock_astream(*args, **kwargs):
            chunks = ["This ", "is ", "a ", "test ", "response."]
            for chunk in chunks:
                yield AIMessage(content=chunk)

        mock.astream = mock_astream

        # Mock bind_tools for tool-enabled LLM (returns self, not async)
        mock.bind_tools = MagicMock(return_value=mock)

        return mock

    @staticmethod
    def create_mock_router_llm():
        """Create a mock router LLM for classification."""
        mock = AsyncMock()

        mock.ainvoke = AsyncMock(return_value=AIMessage(content="SIMPLE"))

        return mock
