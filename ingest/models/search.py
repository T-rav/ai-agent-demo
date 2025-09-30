"""
Search-related Pydantic models.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SearchResult(BaseModel):
    """A search result from vector database."""
    model_config = ConfigDict(
        validate_assignment=True
    )
    
    id: str = Field(..., min_length=1, description="Chunk identifier")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    metadata: Dict[str, Any] = Field(..., description="Chunk metadata")
    
    @field_validator('score')
    @classmethod
    def validate_score(cls, v: float) -> float:
        """Validate similarity score is reasonable."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v
