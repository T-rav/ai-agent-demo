"""
Vector store service for RAG retrieval using Pinecone.
"""

from typing import List, Optional

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from config import settings


class VectorStoreService:
    """Service for interacting with the Pinecone vector store."""

    def __init__(self):
        """Initialize the vector store service."""
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.openai_api_key, model=settings.embedding_model
        )
        self.index_name = settings.pinecone_index_name
        self._vectorstore: Optional[PineconeVectorStore] = None

    def _ensure_index_exists(self):
        """Ensure the Pinecone index exists."""
        # Check if index exists, create if not
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            # Index doesn't exist - it should be created by the ingest pipeline
            raise ValueError(
                f"Index '{self.index_name}' not found. Please run the ingestion pipeline first."
            )

    @property
    def vectorstore(self) -> PineconeVectorStore:
        """Get or create the vector store instance."""
        if self._vectorstore is None:
            self._ensure_index_exists()
            # Use langchain-pinecone which properly supports Pinecone v3+
            # Note: text_key must match the metadata field from ingestion
            self._vectorstore = PineconeVectorStore(
                index_name=self.index_name,
                embedding=self.embeddings,
                pinecone_api_key=settings.pinecone_api_key,
                text_key="content_preview",  # Match the field name from ingestion
            )
        return self._vectorstore

    async def similarity_search(self, query: str, k: int = None) -> List[Document]:
        """
        Perform similarity search in the vector store.

        Args:
            query: The search query
            k: Number of results to return (defaults to settings.retrieval_k)

        Returns:
            List of relevant documents
        """
        k = k or settings.retrieval_k

        # Stub: Perform similarity search
        # In production, this would query Pinecone
        results = self.vectorstore.similarity_search(query, k=k)

        return results

    async def similarity_search_with_score(
        self, query: str, k: int = None
    ) -> List[tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.

        Args:
            query: The search query
            k: Number of results to return

        Returns:
            List of (document, score) tuples
        """
        k = k or settings.retrieval_k

        # Stub: Perform similarity search with scores
        results = self.vectorstore.similarity_search_with_score(query, k=k)

        return results


# Global vector store instance
vector_store_service = VectorStoreService()
