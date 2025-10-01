"""
ChatResponse Pydantic model.
"""

from typing import List, Optional

from pydantic import BaseModel, Field

from .source_document import SourceDocument


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    message: str = Field(..., description="The assistant's response or research report")
    sources: List[SourceDocument] = Field(
        default_factory=list,
        description="Source documents used in generating the response",
    )
    session_id: Optional[str] = Field(None, description="Session ID")
    research_steps: Optional[List[str]] = Field(
        None, description="Steps taken during research process (for research mode)"
    )
