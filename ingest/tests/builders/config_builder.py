"""
Fluent builder for IngestionConfig objects.
"""

from ...models import IngestionConfig


class IngestionConfigBuilder:
    """Fluent builder for IngestionConfig objects."""
    
    def __init__(self):
        self._openai_api_key = "test-openai-key"
        self._pinecone_api_key = "test-pinecone-key"
        self._pinecone_environment = "test-env"
        self._index_name = "test-index"
        self._model = "text-embedding-3-small"
        self._dimensions = 1536
        self._chunk_size = 1000
        self._chunk_overlap = 200
        self._min_chunk_size = 100
        self._max_chunk_size = 2000
        self._embedding_batch_size = 100
        self._upsert_batch_size = 100
        self._corpus_path = "data/corpus"
        self._level = "INFO"
        self._show_progress = True
    
    def with_openai_key(self, key: str) -> 'IngestionConfigBuilder':
        """Set the OpenAI API key."""
        self._openai_api_key = key
        return self
    
    def with_pinecone_key(self, key: str) -> 'IngestionConfigBuilder':
        """Set the Pinecone API key."""
        self._pinecone_api_key = key
        return self
    
    def with_pinecone_environment(self, env: str) -> 'IngestionConfigBuilder':
        """Set the Pinecone environment."""
        self._pinecone_environment = env
        return self
    
    def with_index_name(self, name: str) -> 'IngestionConfigBuilder':
        """Set the index name."""
        self._index_name = name
        return self
    
    def with_embedding_model(self, model: str) -> 'IngestionConfigBuilder':
        """Set the embedding model."""
        self._model = model
        return self
    
    def with_dimensions(self, dimensions: int) -> 'IngestionConfigBuilder':
        """Set the embedding dimensions."""
        self._dimensions = dimensions
        return self
    
    def with_chunk_size(self, size: int) -> 'IngestionConfigBuilder':
        """Set the chunk size."""
        self._chunk_size = size
        return self
    
    def with_chunk_overlap(self, overlap: int) -> 'IngestionConfigBuilder':
        """Set the chunk overlap."""
        self._chunk_overlap = overlap
        return self
    
    def with_corpus_path(self, path: str) -> 'IngestionConfigBuilder':
        """Set the corpus path."""
        self._corpus_path = path
        return self
    
    def with_log_level(self, level: str) -> 'IngestionConfigBuilder':
        """Set the log level."""
        self._level = level
        return self
    
    def with_progress_display(self, show: bool) -> 'IngestionConfigBuilder':
        """Set whether to show progress."""
        self._show_progress = show
        return self
    
    def for_large_embeddings(self) -> 'IngestionConfigBuilder':
        """Configure for large embedding model."""
        return (self.with_embedding_model("text-embedding-3-large")
                   .with_dimensions(3072))
    
    def for_small_embeddings(self) -> 'IngestionConfigBuilder':
        """Configure for small embedding model."""
        return (self.with_embedding_model("text-embedding-3-small")
                   .with_dimensions(1536))
    
    def for_production(self) -> 'IngestionConfigBuilder':
        """Configure for production environment."""
        return (self.with_log_level("WARNING")
                   .with_progress_display(False)
                   .with_chunk_size(1500)
                   .with_chunk_overlap(300))
    
    def for_development(self) -> 'IngestionConfigBuilder':
        """Configure for development environment."""
        return (self.with_log_level("DEBUG")
                   .with_progress_display(True)
                   .with_chunk_size(500)
                   .with_chunk_overlap(100))
    
    def build(self) -> IngestionConfig:
        """Build the IngestionConfig."""
        return IngestionConfig(
            openai_api_key=self._openai_api_key,
            pinecone_api_key=self._pinecone_api_key,
            pinecone_environment=self._pinecone_environment,
            index_name=self._index_name,
            model=self._model,
            dimensions=self._dimensions,
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            min_chunk_size=self._min_chunk_size,
            max_chunk_size=self._max_chunk_size,
            embedding_batch_size=self._embedding_batch_size,
            upsert_batch_size=self._upsert_batch_size,
            corpus_path=self._corpus_path,
            level=self._level,
            show_progress=self._show_progress
        )
