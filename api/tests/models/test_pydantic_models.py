"""
Additional tests for Pydantic models to increase coverage.
"""


from models import ChatMessage, ChatRequest, SourceDocument, StreamChunk


class TestChatMessageEdgeCases:
    """Edge case tests for ChatMessage model."""

    def test_chat_message_with_very_long_content(self):
        """Test message with very long content."""
        long_content = "a" * 10000
        msg = ChatMessage(role="user", content=long_content)

        assert len(msg.content) == 10000

    def test_chat_message_with_special_characters(self):
        """Test message with special characters."""
        msg = ChatMessage(role="user", content="Test 🚀 with émojis and ñ")

        assert "🚀" in msg.content
        assert "ñ" in msg.content


class TestChatRequestEdgeCases:
    """Edge case tests for ChatRequest model."""

    def test_request_with_empty_history(self):
        """Test request with explicitly empty history."""
        request = ChatRequest(message="Test", conversation_history=[], session_id="test-123")

        assert request.conversation_history == []

    def test_request_with_long_session_id(self):
        """Test request with long session ID."""
        long_id = "session-" + "x" * 100
        request = ChatRequest(message="Test", session_id=long_id)

        assert request.session_id == long_id

    def test_request_research_mode_defaults_false(self):
        """Test that research mode defaults to False."""
        request = ChatRequest(message="Test", session_id="test-123")

        assert request.research_mode is False


class TestSourceDocumentModel:
    """Tests for SourceDocument model."""

    def test_source_document_with_minimal_data(self):
        """Test source document with minimal required data."""
        doc = SourceDocument(content="Test content", metadata={"source": "test.md"})

        assert doc.content == "Test content"
        assert doc.metadata["source"] == "test.md"
        assert doc.score is None

    def test_source_document_with_score(self):
        """Test source document with relevance score."""
        doc = SourceDocument(content="Test content", metadata={"source": "test.md"}, score=0.95)

        assert doc.score == 0.95

    def test_source_document_serialization(self):
        """Test source document can be serialized."""
        doc = SourceDocument(
            content="Test content", metadata={"source": "test.md", "title": "Test"}, score=0.85
        )

        json_data = doc.model_dump()
        assert json_data["content"] == "Test content"
        assert json_data["metadata"]["source"] == "test.md"
        assert json_data["score"] == 0.85


class TestStreamChunkModel:
    """Tests for StreamChunk model."""

    def test_stream_chunk_token_type(self):
        """Test stream chunk with token type."""
        chunk = StreamChunk(type="token", content="Hello world")

        assert chunk.type == "token"
        assert chunk.content == "Hello world"

    def test_stream_chunk_sources_type(self):
        """Test stream chunk with sources type."""
        source_doc = SourceDocument(content="Test content", metadata={"source": "test.md"})
        chunk = StreamChunk(type="sources", sources=[source_doc])

        assert chunk.type == "sources"
        assert len(chunk.sources) == 1
        assert chunk.sources[0].content == "Test content"

    def test_stream_chunk_error_type(self):
        """Test stream chunk with error type."""
        chunk = StreamChunk(type="error", error="Something went wrong")

        assert chunk.type == "error"
        assert chunk.error == "Something went wrong"

    def test_stream_chunk_json_serialization(self):
        """Test stream chunk JSON serialization."""
        chunk = StreamChunk(type="token", content="Test")

        json_str = chunk.model_dump_json()
        assert "token" in json_str
        assert "Test" in json_str
