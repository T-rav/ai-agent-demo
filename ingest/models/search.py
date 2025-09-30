"""
Search - related Pydantic models.
"""

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field


class SearchResult(BaseModel):
    """A search result from vector database."""

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(..., min_length=1, description="Chunk identifier")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    metadata: Dict[str, Any] = Field(..., description="Chunk metadata")
