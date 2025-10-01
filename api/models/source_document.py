"""
SourceDocument Pydantic model.
"""

from typing import Optional

from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    """A source document from RAG retrieval."""

    content: str = Field(..., description="The content of the source document")
    metadata: dict = Field(default_factory=dict, description="Metadata about the source")
    score: Optional[float] = Field(None, description="Relevance score")
