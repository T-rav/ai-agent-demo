"""
Pinecone client and vector database operations.
Handles index management, embedding generation, and vector upserts.
"""

import time
from typing import Any, Dict, List, Optional

from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm


class PineconeVectorStore:
    """Manages Pinecone vector database operations."""

    def __init__(
        self,
        api_key: str,
        environment: str,
        index_name: str,
        embedding_model: str = "text-embedding-3-small",
        embedding_dimensions: int = 1536,
    ):
        """
        Initialize Pinecone client and configuration.

        Args:
            api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Name of the Pinecone index
            embedding_model: OpenAI embedding model name
            embedding_dimensions: Embedding vector dimensions
        """
        self.pc = Pinecone(api_key=api_key)
        self.environment = environment
        self.index_name = index_name
        self.embedding_model = embedding_model
        self.embedding_dimensions = embedding_dimensions
        self.openai_client = OpenAI()
        self.index = None

    def create_index_if_not_exists(self) -> None:
        """Create Pinecone index if it doesn't exist."""
        existing_indexes = [index.name for index in self.pc.list_indexes()]

        if self.index_name not in existing_indexes:
            print(f"Creating index '{self.index_name}'...")
            self.pc.create_index(
                name=self.index_name,
                dimension=self.embedding_dimensions,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

            # Wait for index to be ready
            while not self.pc.describe_index(self.index_name).status["ready"]:
                print("Waiting for index to be ready...")
                time.sleep(1)

            print(f"Index '{self.index_name}' created successfully!")
        else:
            print(f"Index '{self.index_name}' already exists.")

        self.index = self.pc.Index(self.index_name)

    def generate_embeddings(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI.

        Args:
            texts: List of text strings to embed
            batch_size: Number of texts to process in each batch

        Returns:
            List of embedding vectors
        """
        embeddings = []

        print(f"Generating embeddings for {len(texts)} texts...")

        for i in tqdm(range(0, len(texts), batch_size), desc="Embedding batches"):
            batch = texts[i : i + batch_size]

            try:
                response = self.openai_client.embeddings.create(model=self.embedding_model, input=batch)

                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)

            except Exception as e:
                print(f"Error generating embeddings for batch {i // batch_size + 1}: {str(e)}")
                # Add empty embeddings for failed batch
                embeddings.extend([[0.0] * self.embedding_dimensions] * len(batch))

        return embeddings

    def upsert_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 100) -> None:
        """
        Upsert document chunks into Pinecone index.

        Args:
            chunks: List of chunk dictionaries with content and metadata
            batch_size: Number of vectors to upsert in each batch
        """
        if not self.index:
            raise ValueError("Index not initialized. Call create_index_if_not_exists() first.")

        # Extract and clean text content for embedding
        texts = []
        for chunk in chunks:
            # Clean text: normalize whitespace, remove excessive newlines
            clean_text = chunk.content.replace("\n", " ").replace("\r", " ")
            # Normalize multiple spaces to single space
            clean_text = " ".join(clean_text.split())
            texts.append(clean_text)

        # Generate embeddings
        embeddings = self.generate_embeddings(texts)

        # Prepare vectors for upsert
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Filter out None values from metadata for Pinecone compatibility
            metadata = {k: v for k, v in chunk.metadata.model_dump().items() if v is not None}

            # Clean content preview (normalize whitespace like we do for embeddings)
            clean_preview = chunk.content.replace("\n", " ").replace("\r", " ")
            clean_preview = " ".join(clean_preview.split())
            metadata["content_preview"] = clean_preview[:500] + "..." if len(clean_preview) > 500 else clean_preview

            vector = {
                "id": chunk.id,
                "values": embedding,
                "metadata": metadata,
            }
            vectors.append(vector)

        # Upsert in batches
        print(f"Upserting {len(vectors)} vectors to Pinecone...")

        for i in tqdm(range(0, len(vectors), batch_size), desc="Upsert batches"):
            batch = vectors[i : i + batch_size]

            try:
                self.index.upsert(vectors=batch)
            except Exception as e:
                print(f"Error upserting batch {i // batch_size + 1}: {str(e)}")

        print(f"Successfully upserted {len(vectors)} vectors!")

    def query_similar(
        self, query_text: str, top_k: int = 10, filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query for similar vectors in the index.

        Args:
            query_text: Text to search for
            top_k: Number of results to return
            filter_dict: Optional metadata filter

        Returns:
            List of similar chunks with scores
        """
        if not self.index:
            raise ValueError("Index not initialized. Call create_index_if_not_exists() first.")

        # Generate embedding for query
        query_embedding = self.generate_embeddings([query_text])[0]

        # Query the index
        results = self.index.query(vector=query_embedding, top_k=top_k, filter=filter_dict, include_metadata=True)

        return [{"id": match.id, "score": match.score, "metadata": match.metadata} for match in results.matches]

    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the current index."""
        if not self.index:
            raise ValueError("Index not initialized. Call create_index_if_not_exists() first.")

        stats = self.index.describe_index_stats()
        return {
            "total_vector_count": stats.total_vector_count,
            "dimension": stats.dimension,
            "index_fullness": stats.index_fullness,
            "namespaces": dict(stats.namespaces) if stats.namespaces else {},
        }

    def delete_all_vectors(self) -> None:
        """Delete all vectors from the index. Use with caution!"""
        if not self.index:
            raise ValueError("Index not initialized. Call create_index_if_not_exists() first.")

        print("Deleting all vectors from index...")
        self.index.delete(delete_all=True)
        print("All vectors deleted!")
