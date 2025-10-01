"""
ChatRequest Pydantic model.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from .chat_message import ChatMessage


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, description="The user's message or research topic")
    conversation_history: List[ChatMessage] = Field(
        default_factory=list, description="Previous conversation history"
    )
    session_id: Optional[str] = Field(None, description="Optional session ID for tracking")
    research_mode: bool = Field(
        default=False, description="If True, activates deep research mode for comprehensive reports"
    )
