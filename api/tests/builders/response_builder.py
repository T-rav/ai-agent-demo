"""
Fluent builders for API response objects.
"""

from typing import List, Optional

from models import ChatResponse, SourceDocument, StreamChunk


class SourceDocumentBuilder:
    """Fluent builder for SourceDocument objects."""

    def __init__(self):
        self._content = "Test source content"
        self._metadata = {"source": "test.md", "title": "Test Document"}
        self._score = 0.95

    def with_content(self, content: str) -> "SourceDocumentBuilder":
        """Set the source content."""
        self._content = content
        return self

    def with_metadata(self, metadata: dict) -> "SourceDocumentBuilder":
        """Set the metadata."""
        self._metadata = metadata
        return self

    def with_score(self, score: float) -> "SourceDocumentBuilder":
        """Set the relevance score."""
        self._score = score
        return self

    def with_source(self, source: str) -> "SourceDocumentBuilder":
        """Set the source file."""
        self._metadata["source"] = source
        return self

    def with_title(self, title: str) -> "SourceDocumentBuilder":
        """Set the document title."""
        self._metadata["title"] = title
        return self

    def as_rag_document(self) -> "SourceDocumentBuilder":
        """Configure as a RAG-related document."""
        return (
            self.with_content("RAG combines retrieval with generation for better responses.")
            .with_source("rag_overview.md")
            .with_title("RAG Systems Overview")
            .with_score(0.92)
        )

    def as_vector_db_document(self) -> "SourceDocumentBuilder":
        """Configure as a vector database document."""
        return (
            self.with_content("Vector databases store embeddings for semantic search.")
            .with_source("vector_db.md")
            .with_title("Vector Databases")
            .with_score(0.88)
        )

    def build(self) -> SourceDocument:
        """Build the SourceDocument."""
        return SourceDocument(content=self._content, metadata=self._metadata, score=self._score)


class ChatResponseBuilder:
    """Fluent builder for ChatResponse objects."""

    def __init__(self):
        self._message = "This is a test response."
        self._sources = []
        self._session_id = None
        self._research_steps = None

    def with_message(self, message: str) -> "ChatResponseBuilder":
        """Set the response message."""
        self._message = message
        return self

    def with_sources(self, sources: List[SourceDocument]) -> "ChatResponseBuilder":
        """Set the source documents."""
        self._sources = sources
        return self

    def with_session_id(self, session_id: str) -> "ChatResponseBuilder":
        """Set the session ID."""
        self._session_id = session_id
        return self

    def with_research_steps(self, steps: List[str]) -> "ChatResponseBuilder":
        """Set the research steps."""
        self._research_steps = steps
        return self

    def with_rag_sources(self) -> "ChatResponseBuilder":
        """Add typical RAG sources."""
        self._sources = [
            a_source_document().as_rag_document().build(),
            a_source_document().as_vector_db_document().build(),
        ]
        return self

    def build(self) -> ChatResponse:
        """Build the ChatResponse."""
        return ChatResponse(
            message=self._message,
            sources=self._sources,
            session_id=self._session_id,
            research_steps=self._research_steps,
        )


class StreamChunkBuilder:
    """Fluent builder for StreamChunk objects."""

    def __init__(self):
        self._type = "token"
        self._content = None
        self._sources = None
        self._error = None
        self._step = None

    def with_type(self, chunk_type: str) -> "StreamChunkBuilder":
        """Set the chunk type."""
        self._type = chunk_type
        return self

    def with_content(self, content: str) -> "StreamChunkBuilder":
        """Set the content."""
        self._content = content
        return self

    def with_sources(self, sources: List[SourceDocument]) -> "StreamChunkBuilder":
        """Set the sources."""
        self._sources = sources
        return self

    def with_error(self, error: str) -> "StreamChunkBuilder":
        """Set the error message."""
        self._error = error
        return self

    def with_step(self, step: str) -> "StreamChunkBuilder":
        """Set the research step."""
        self._step = step
        return self

    def as_token(self, content: str = "Test ") -> "StreamChunkBuilder":
        """Configure as a token chunk."""
        return self.with_type("token").with_content(content)

    def as_sources(self) -> "StreamChunkBuilder":
        """Configure as a sources chunk."""
        sources = [a_source_document().as_rag_document().build()]
        return self.with_type("sources").with_sources(sources)

    def as_done(self) -> "StreamChunkBuilder":
        """Configure as a done chunk."""
        return self.with_type("done")

    def as_error(self, error: str = "Test error") -> "StreamChunkBuilder":
        """Configure as an error chunk."""
        return self.with_type("error").with_error(error)

    def as_step(self, step: str = "Gathering information") -> "StreamChunkBuilder":
        """Configure as a step chunk."""
        return self.with_type("step").with_step(step)

    def build(self) -> StreamChunk:
        """Build the StreamChunk."""
        return StreamChunk(
            type=self._type,
            content=self._content,
            sources=self._sources,
            error=self._error,
            step=self._step,
        )


def a_source_document() -> SourceDocumentBuilder:
    """Create a new SourceDocument builder."""
    return SourceDocumentBuilder()


def a_chat_response() -> ChatResponseBuilder:
    """Create a new ChatResponse builder."""
    return ChatResponseBuilder()


def a_stream_chunk() -> StreamChunkBuilder:
    """Create a new StreamChunk builder."""
    return StreamChunkBuilder()
