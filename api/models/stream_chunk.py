"""
StreamChunk Pydantic model.
"""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .source_document import SourceDocument


class StreamChunk(BaseModel):
    """A chunk of streaming response."""

    type: Literal["token", "sources", "done", "error", "step"] = Field(
        ..., description="Type of chunk"
    )
    content: Optional[str] = Field(None, description="Content for token chunks")
    sources: Optional[List[dict]] = Field(None, description="Sources for sources chunks")
    error: Optional[str] = Field(None, description="Error message for error chunks")
    step: Optional[str] = Field(None, description="Research step description (for research mode)")
