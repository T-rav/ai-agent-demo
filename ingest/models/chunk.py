"""
Chunk - related Pydantic models.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import FileType


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk with validation."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, frozen=True)

    file_name: str = Field(..., min_length=1, description="Name of the source file")
    file_type: FileType = Field(..., description="Type of the source document")
    document_title: str = Field(..., min_length=1, description="Title of the source document")
    chunk_index: int = Field(..., ge=0, description="Index of this chunk within the document")
    token_count: int = Field(..., ge=0, description="Number of tokens in this chunk")
    char_count: int = Field(..., ge=0, description="Number of characters in this chunk")
    section_header: Optional[str] = Field(None, description="Section header if applicable")
    page_number: Optional[int] = Field(None, ge=1, description="Page number if applicable")


class DocumentChunk(BaseModel):
    """A document chunk with content and metadata."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    id: str = Field(..., min_length=1, description="Unique identifier for the chunk")
    content: str = Field(..., min_length=1, description="Text content of the chunk")
    metadata: ChunkMetadata = Field(..., description="Metadata about the chunk")

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate chunk ID format."""
        if not v or not v.strip():
            raise ValueError("Chunk ID cannot be empty")
        # Basic validation - could be more specific
        if len(v) > 200:
            raise ValueError("Chunk ID too long")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate that content is not empty."""
        if not v or not v.strip():
            raise ValueError("Chunk content cannot be empty")
        return v
