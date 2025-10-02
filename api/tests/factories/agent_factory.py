"""
Factory for creating agent test doubles.
"""

from unittest.mock import AsyncMock


class AgentFactory:
    """Factory methods for creating agent test doubles."""

    @staticmethod
    def create_mock_agent():
        """Create a mock RAG agent."""
        mock = AsyncMock()

        # Mock astream for streaming responses
        async def mock_astream(messages, session_id=None):
            yield {"type": "token", "content": "Test "}
            yield {"type": "token", "content": "response."}
            yield {"type": "done"}

        mock.astream = mock_astream

        # Mock ainvoke for non-streaming responses
        mock.ainvoke = AsyncMock(
            return_value={"message": "Test response from agent.", "sources": []}
        )

        return mock

    @staticmethod
    def create_mock_agent_with_sources():
        """Create a mock agent that returns sources."""
        mock = AsyncMock()

        async def mock_astream(messages, session_id=None):
            yield {"type": "token", "content": "RAG "}
            yield {"type": "token", "content": "response "}
            yield {"type": "token", "content": "with sources."}
            yield {
                "type": "sources",
                "sources": [
                    {
                        "content": "RAG combines retrieval with generation.",
                        "metadata": {"source": "rag.md", "title": "RAG Overview"},
                        "score": 0.95,
                    }
                ],
            }
            yield {"type": "done"}

        mock.astream = mock_astream

        mock.ainvoke = AsyncMock(
            return_value={
                "message": "RAG combines retrieval with generation for better responses.",
                "sources": [
                    {
                        "content": "RAG combines retrieval with generation.",
                        "metadata": {"source": "rag.md", "title": "RAG Overview"},
                        "score": 0.95,
                    }
                ],
            }
        )

        return mock

    @staticmethod
    def create_mock_agent_with_error():
        """Create a mock agent that raises an error."""
        mock = AsyncMock()

        async def mock_error_stream(messages, session_id=None):
            raise Exception("Agent processing error")

        mock.astream = mock_error_stream
        mock.ainvoke = AsyncMock(side_effect=Exception("Agent processing error"))

        return mock
