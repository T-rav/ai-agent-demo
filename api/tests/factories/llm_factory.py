"""
Factory for creating LLM test doubles.
"""

from unittest.mock import AsyncMock

from langchain_core.messages import AIMessage


class LLMFactory:
    """Factory methods for creating LLM test doubles."""

    @staticmethod
    def create_mock_llm(response_content="This is a test response from the LLM."):
        """
        Create a mock LLM with configurable response.

        Args:
            response_content: The content the LLM should return

        Returns:
            Mock LLM configured with the specified response
        """
        from unittest.mock import MagicMock

        mock = MagicMock()

        # Mock ainvoke with configurable response
        mock.ainvoke = AsyncMock(return_value=AIMessage(content=response_content))

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
    def create_mock_router_llm(decision="SIMPLE"):
        """
        Create a mock router LLM for classification.

        Args:
            decision: The routing decision to return (SIMPLE or RESEARCH)

        Returns:
            Mock router LLM configured with the specified decision
        """
        mock = AsyncMock()

        mock.ainvoke = AsyncMock(return_value=AIMessage(content=decision))

        return mock
