"""
Fluent builders for API request objects.
"""

from typing import List

from models import ChatMessage, ChatRequest


class ChatMessageBuilder:
    """Fluent builder for ChatMessage objects."""

    def __init__(self):
        self._role = "user"
        self._content = "Test message"

    def with_role(self, role: str) -> "ChatMessageBuilder":
        """Set the message role."""
        self._role = role
        return self

    def with_content(self, content: str) -> "ChatMessageBuilder":
        """Set the message content."""
        self._content = content
        return self

    def as_user(self) -> "ChatMessageBuilder":
        """Configure as a user message."""
        return self.with_role("user")

    def as_assistant(self) -> "ChatMessageBuilder":
        """Configure as an assistant message."""
        return self.with_role("assistant")

    def as_system(self) -> "ChatMessageBuilder":
        """Configure as a system message."""
        return self.with_role("system")

    def build(self) -> ChatMessage:
        """Build the ChatMessage."""
        return ChatMessage(role=self._role, content=self._content)


class ChatRequestBuilder:
    """Fluent builder for ChatRequest objects."""

    def __init__(self):
        self._message = "What is RAG?"
        self._conversation_history = []
        self._session_id = None
        self._research_mode = False

    def with_message(self, message: str) -> "ChatRequestBuilder":
        """Set the user message."""
        self._message = message
        return self

    def with_conversation_history(self, history: List[ChatMessage]) -> "ChatRequestBuilder":
        """Set the conversation history."""
        self._conversation_history = history
        return self

    def with_session_id(self, session_id: str) -> "ChatRequestBuilder":
        """Set the session ID."""
        self._session_id = session_id
        return self

    def with_research_mode(self, enabled: bool = True) -> "ChatRequestBuilder":
        """Enable or disable research mode."""
        self._research_mode = enabled
        return self

    def with_history(self, *messages: ChatMessage) -> "ChatRequestBuilder":
        """Add messages to conversation history."""
        self._conversation_history = list(messages)
        return self

    def with_simple_history(self) -> "ChatRequestBuilder":
        """Add a simple conversation history."""
        self._conversation_history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi! How can I help you?"),
        ]
        return self

    def build(self) -> ChatRequest:
        """Build the ChatRequest."""
        return ChatRequest(
            message=self._message,
            conversation_history=self._conversation_history,
            session_id=self._session_id,
            research_mode=self._research_mode,
        )


def a_chat_message() -> ChatMessageBuilder:
    """Create a new ChatMessage builder."""
    return ChatMessageBuilder()


def a_chat_request() -> ChatRequestBuilder:
    """Create a new ChatRequest builder."""
    return ChatRequestBuilder()
