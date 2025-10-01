"""
Configuration Pydantic model.
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class IngestionConfig(BaseModel):
    """Configuration for the ingestion process."""

    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)

    # API Configuration
    openai_api_key: str = Field(..., min_length=1, description="OpenAI API key")
    pinecone_api_key: str = Field(..., min_length=1, description="Pinecone API key")
    pinecone_environment: str = Field(..., min_length=1, description="Pinecone environment")

    # Database Configuration
    index_name: str = Field(
        default="ai - agent - demo - index",
        min_length=1,
        description="Pinecone index name",
    )

    # Embedding Configuration
    model: str = Field(
        default="text - embedding - 3-small",
        min_length=1,
        description="OpenAI embedding model",
    )
    dimensions: int = Field(default=1536, gt=0, description="Embedding dimensions")

    # Processing Configuration
    chunk_size: int = Field(default=1000, gt=0, le=8000, description="Target tokens per chunk")
    chunk_overlap: int = Field(default=200, ge=0, description="Overlapping tokens between chunks")
    min_chunk_size: int = Field(default=100, gt=0, description="Minimum chunk size in tokens")
    max_chunk_size: int = Field(default=2000, gt=0, description="Maximum chunk size in tokens")
    embedding_batch_size: int = Field(
        default=100, gt=0, le=1000, description="Batch size for embeddings"
    )
    upsert_batch_size: int = Field(
        default=100, gt=0, le=1000, description="Batch size for vector upserts"
    )

    # Path Configuration
    corpus_path: str = Field(
        default="data / corpus", min_length=1, description="Path to corpus directory"
    )

    # Logging Configuration
    level: str = Field(default="INFO", description="Logging level")
    show_progress: bool = Field(default=True, description="Show progress bars")

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Validate chunk overlap is reasonable compared to chunk size."""
        # Note: In Pydantic v2, we can't easily access other fields during validation
        # This would need to be a model validator if we want to compare fields
        if v < 0:
            raise ValueError("Chunk overlap cannot be negative")
        return v

    @field_validator("min_chunk_size", "max_chunk_size")
    @classmethod
    def validate_chunk_sizes(cls, v: int) -> int:
        """Validate chunk sizes are reasonable."""
        if v <= 0:
            raise ValueError("Chunk sizes must be positive")
        return v
