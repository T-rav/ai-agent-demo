"""
Document - related Pydantic models.
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import FileType


class DocumentMetadata(BaseModel):
    """Metadata for a processed document with validation."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, frozen=True)

    file_name: str = Field(..., min_length=1, description="Name of the file")
    file_type: FileType = Field(..., description="Type of the document file")
    title: str = Field(..., min_length=1, description="Extracted document title")
    token_count: int = Field(..., ge=0, description="Number of tokens in the document")
    char_count: int = Field(..., ge=0, description="Number of characters in the document")


class ProcessedDocument(BaseModel):
    """A fully processed document with content and metadata."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    file_name: str = Field(..., min_length=1, description="Name of the file")
    file_type: FileType = Field(..., description="Type of the document file")
    title: str = Field(..., min_length=1, description="Extracted document title")
    content: str = Field(..., min_length=1, description="Processed document content")
    token_count: int = Field(..., ge=0, description="Number of tokens in the document")
    char_count: int = Field(..., ge=0, description="Number of characters in the document")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Validate that content is not empty."""
        if not v or not v.strip():
            raise ValueError("Document content cannot be empty")
        return v

    def to_metadata(self) -> DocumentMetadata:
        """Convert to DocumentMetadata."""
        return DocumentMetadata(
            file_name=self.file_name,
            file_type=self.file_type,
            title=self.title,
            token_count=self.token_count,
            char_count=self.char_count,
        )
