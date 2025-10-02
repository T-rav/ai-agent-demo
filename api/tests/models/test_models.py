"""
Tests for Pydantic models.
"""

import pytest
from pydantic import ValidationError

from models import ChatMessage, ChatRequest, ChatResponse, SourceDocument, StreamChunk


class TestChatMessage:
    """Tests for ChatMessage model."""

    def test_create_user_message(self):
        """Test creating a user message."""
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_create_assistant_message(self):
        """Test creating an assistant message."""
        msg = ChatMessage(role="assistant", content="Hi there!")
        assert msg.role == "assistant"
        assert msg.content == "Hi there!"

    def test_invalid_role(self):
        """Test that invalid role raises error."""
        with pytest.raises(ValidationError):
            ChatMessage(role="invalid", content="Test")

    def test_empty_content(self):
        """Test that empty content is allowed."""
        msg = ChatMessage(role="user", content="")
        assert msg.content == ""


class TestChatRequest:
    """Tests for ChatRequest model."""

    def test_create_simple_request(self):
        """Test creating a simple chat request."""
        req = ChatRequest(message="What is RAG?")
        assert req.message == "What is RAG?"
        assert req.conversation_history == []
        assert req.session_id is None
        assert req.research_mode is False

    def test_create_request_with_history(self):
        """Test creating request with conversation history."""
        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi!"),
        ]
        req = ChatRequest(message="Tell me more", conversation_history=history)
        assert len(req.conversation_history) == 2
        assert req.conversation_history[0].role == "user"

    def test_request_with_session_id(self):
        """Test request with session ID."""
        req = ChatRequest(message="Test", session_id="session-123")
        assert req.session_id == "session-123"

    def test_research_mode(self):
        """Test research mode flag."""
        req = ChatRequest(message="Research AI", research_mode=True)
        assert req.research_mode is True

    def test_empty_message_validation(self):
        """Test that empty message is rejected."""
        with pytest.raises(ValidationError):
            ChatRequest(message="")


class TestSourceDocument:
    """Tests for SourceDocument model."""

    def test_create_source_document(self):
        """Test creating a source document."""
        doc = SourceDocument(
            content="Test content",
            metadata={"source": "test.md", "title": "Test"},
            score=0.95,
        )
        assert doc.content == "Test content"
        assert doc.metadata["source"] == "test.md"
        assert doc.score == 0.95

    def test_source_document_defaults(self):
        """Test source document with default values."""
        doc = SourceDocument(content="Test")
        assert doc.metadata == {}
        assert doc.score is None


class TestChatResponse:
    """Tests for ChatResponse model."""

    def test_create_response(self):
        """Test creating a chat response."""
        sources = [SourceDocument(content="Source", metadata={}, score=0.9)]
        resp = ChatResponse(message="Response message", sources=sources, session_id="session-123")
        assert resp.message == "Response message"
        assert len(resp.sources) == 1
        assert resp.session_id == "session-123"

    def test_response_with_research_steps(self):
        """Test response with research steps."""
        resp = ChatResponse(message="Research report", research_steps=["Step 1", "Step 2"])
        assert len(resp.research_steps) == 2

    def test_response_defaults(self):
        """Test response with default values."""
        resp = ChatResponse(message="Test")
        assert resp.sources == []
        assert resp.session_id is None
        assert resp.research_steps is None


class TestStreamChunk:
    """Tests for StreamChunk model."""

    def test_token_chunk(self):
        """Test creating a token chunk."""
        chunk = StreamChunk(type="token", content="Hello")
        assert chunk.type == "token"
        assert chunk.content == "Hello"

    def test_sources_chunk(self):
        """Test creating a sources chunk."""
        sources = [{"content": "Test", "metadata": {}, "score": 0.9}]
        chunk = StreamChunk(type="sources", sources=sources)
        assert chunk.type == "sources"
        assert len(chunk.sources) == 1

    def test_done_chunk(self):
        """Test creating a done chunk."""
        chunk = StreamChunk(type="done")
        assert chunk.type == "done"
        assert chunk.content is None

    def test_error_chunk(self):
        """Test creating an error chunk."""
        chunk = StreamChunk(type="error", error="Something went wrong")
        assert chunk.type == "error"
        assert chunk.error == "Something went wrong"

    def test_step_chunk(self):
        """Test creating a step chunk."""
        chunk = StreamChunk(type="step", step="Gathering information")
        assert chunk.type == "step"
        assert chunk.step == "Gathering information"

    def test_invalid_type(self):
        """Test that invalid type raises error."""
        with pytest.raises(ValidationError):
            StreamChunk(type="invalid")
