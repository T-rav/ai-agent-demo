"""
Vector store service for RAG retrieval using Pinecone.
"""

from typing import List, Optional

from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

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
        self._vectorstore: Optional[LangchainPinecone] = None

    def _ensure_index_exists(self):
        """Ensure the Pinecone index exists."""
        # Stub: Check if index exists, create if not
        # In production, you'd check existing indexes and create if needed
        pass

    @property
    def vectorstore(self) -> LangchainPinecone:
        """Get or create the vector store instance."""
        if self._vectorstore is None:
            self._ensure_index_exists()
            self._vectorstore = LangchainPinecone.from_existing_index(
                index_name=self.index_name, embedding=self.embeddings
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
