"""
Configuration for the API.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from environment (e.g., langchain internal vars)
    )

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4-turbo-preview", description="OpenAI model to use")

    # Pinecone Configuration
    pinecone_api_key: str = Field(..., description="Pinecone API key")
    pinecone_environment: str = Field(..., description="Pinecone environment")
    pinecone_index_name: str = Field(
        default="ai-agent-demo-index", description="Pinecone index name"
    )

    # Embedding Configuration
    embedding_model: str = Field(default="text-embedding-3-small", description="Embedding model")
    embedding_dimensions: int = Field(default=1536, description="Embedding dimensions")

    # RAG Configuration
    retrieval_k: int = Field(default=5, description="Number of documents to retrieve")
    score_threshold: float = Field(default=0.5, description="Minimum similarity score threshold")

    # Tavily Search Configuration
    tavily_api_key: Optional[str] = Field(None, description="Tavily API key for web search")

    # LangSmith Configuration (for observability)
    langchain_tracing_v2: bool = Field(default=True, description="Enable LangSmith tracing")
    langchain_api_key: Optional[str] = Field(None, description="LangSmith API key")
    langchain_project: str = Field(default="ai-agent-demo", description="LangSmith project name")

    # Application Configuration
    debug: bool = Field(default=False, description="Debug mode")


# Global settings instance
settings = Settings()
