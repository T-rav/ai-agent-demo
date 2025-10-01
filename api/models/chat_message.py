"""
ChatMessage Pydantic model.
"""

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message."""

    role: Literal["user", "assistant", "system"] = Field(
        ..., description="The role of the message sender"
    )
    content: str = Field(..., description="The content of the message")
