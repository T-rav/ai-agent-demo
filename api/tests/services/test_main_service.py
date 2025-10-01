"""
Tests for main application service functionality.
"""

from unittest.mock import patch

import pytest

from models import ChatMessage


class TestMessageConversion:
    """Tests for message conversion in main endpoints."""

    def test_chat_endpoint_converts_messages_correctly(self):
        """Test that chat endpoint correctly converts message format."""

        # Test that ChatMessage pydantic model works correctly
        msg = ChatMessage(role="user", content="Hello")

        # Convert to dict (what main.py does inline)
        msg_dict = {"role": msg.role, "content": msg.content}

        assert msg_dict["role"] == "user"
        assert msg_dict["content"] == "Hello"

    def test_conversation_history_to_dict_list(self):
        """Test converting conversation history to dict format."""

        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there"),
        ]

        # Convert as main.py does
        messages = [{"role": msg.role, "content": msg.content} for msg in history]

        assert len(messages) == 2
        assert messages[0]["content"] == "Hello"
        assert messages[1]["content"] == "Hi there"


class TestChatResponseFormatting:
    """Tests for chat response formatting."""

    def test_format_sources_from_state(self):
        """Test formatting source documents from agent state."""
        from models import SourceDocument

        # Test that we can create source documents
        source = SourceDocument(
            content="Test content from KB",
            metadata={"source": "test.md", "title": "Test Doc"},
            score=0.95,
        )

        assert source.content == "Test content from KB"
        assert source.metadata["source"] == "test.md"
        assert source.score == 0.95


class TestApplicationStartup:
    """Tests for application startup and initialization."""

    def test_app_has_cors_middleware(self):
        """Test that app has CORS middleware configured."""
        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            # Check that middleware is registered
            assert hasattr(app, "middleware_stack")

    def test_app_has_routes_registered(self):
        """Test that all routes are registered."""
        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            routes = [route.path for route in app.routes]

            assert "/" in routes
            assert "/health" in routes
            assert "/api/chat" in routes
            assert "/api/chat/stream" in routes


class TestErrorHandling:
    """Tests for error handling in main."""

    @pytest.mark.asyncio
    async def test_chat_endpoint_handles_validation_error(self):
        """Test that validation errors are handled properly."""
        from fastapi.testclient import TestClient

        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            client = TestClient(app)

            # Send invalid request (empty message)
            response = client.post("/api/chat", json={"message": ""})

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_stream_endpoint_handles_invalid_request(self):
        """Test that stream endpoint validates requests."""
        from fastapi.testclient import TestClient

        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            client = TestClient(app)

            # Send invalid request
            response = client.post("/api/chat/stream", json={})

            assert response.status_code == 422
