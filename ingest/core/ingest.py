#!/usr / bin / env python3
"""
Main ingestion script for processing documents and storing them in Pinecone.
Processes the data corpus from ai - pocket - projects and creates searchable embeddings.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from ..models import DocumentChunk, IngestionConfig, ProcessedDocument
from ..services import DocumentChunkingService, DocumentProcessorService, PineconeVectorStore
from .config_loader import load_config


class CorpusIngester:
    """Main class for ingesting the AI pocket projects corpus."""

    def __init__(self, config: IngestionConfig):
        """Initialize the ingester with configuration."""
        self.config = config
        self.doc_processor = DocumentProcessorService()
        self.chunker = DocumentChunkingService(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            min_chunk_size=config.min_chunk_size,
            max_chunk_size=config.max_chunk_size,
        )
        self.vector_store = PineconeVectorStore(
            api_key=config.pinecone_api_key,
            environment=config.pinecone_environment,
            index_name=config.index_name,
            embedding_model=config.model,
            embedding_dimensions=config.dimensions,
        )

    def discover_documents(self, corpus_path: Path) -> List[Path]:
        """
        Discover all documents in the corpus directory.

        Args:
            corpus_path: Path to the corpus directory

        Returns:
            List of document file paths
        """
        supported_extensions = {".pdf", ".md", ".txt"}
        documents = []

        for root, dirs, files in os.walk(corpus_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in supported_extensions:
                    documents.append(file_path)

        print("Discovered {len(documents)} documents:")
        for doc in sorted(documents):
            print("  - {doc.relative_to(corpus_path)}")

        return documents

    def process_documents(self, document_paths: List[Path]) -> List[ProcessedDocument]:
        """
        Process all documents and extract content.

        Args:
            document_paths: List of document file paths

        Returns:
            List of processed document dictionaries
        """
        documents = []

        print("\nProcessing {len(document_paths)} documents...")

        for doc_path in document_paths:
            print("Processing: {doc_path.name}")

            document = self.doc_processor.process_file(doc_path)
            if document:
                documents.append(document)
            else:
                print("  ⚠️  Failed to process {doc_path.name}")

        print("Successfully processed {len(documents)} documents")
        return documents

    def chunk_documents(self, documents: List[ProcessedDocument]) -> List[DocumentChunk]:
        """
        Chunk all documents for optimal embedding.

        Args:
            documents: List of processed documents

        Returns:
            List of document chunks
        """
        all_chunks = []

        print("\nChunking {len(documents)} documents...")

        for document in documents:
            print("Chunking: {document['file_name']}")

            chunks = self.chunker.chunk_document(document)
            all_chunks.extend(chunks)

            print("  Created {len(chunks)} chunks")

        print("Total chunks created: {len(all_chunks)}")
        return all_chunks

    def ingest_to_pinecone(self, chunks: List[DocumentChunk]) -> None:
        """
        Ingest chunks into Pinecone vector database.

        Args:
            chunks: List of document chunks to ingest
        """
        print("\nIngesting {len(chunks)} chunks to Pinecone...")

        # Create index if it doesn't exist
        self.vector_store.create_index_if_not_exists()

        # Upsert chunks
        self.vector_store.upsert_chunks(chunks, batch_size=self.config.upsert_batch_size)

        # Print final stats
        stats = self.vector_store.get_index_stats()
        print("\nIngestion complete!")
        print("Index stats: {stats}")

    def run_ingestion(self, corpus_path: Path, clean_index: bool = False) -> None:
        """
        Run the complete ingestion pipeline.

        Args:
            corpus_path: Path to the corpus directory
            clean_index: Whether to clean the index before ingestion
        """
        print("🚀 Starting AI Pocket Projects Corpus Ingestion")
        print("=" * 50)

        if clean_index:
            print("🧹 Cleaning existing index...")
            self.vector_store.create_index_if_not_exists()
            self.vector_store.delete_all_vectors()

        # Step 1: Discover documents
        document_paths = self.discover_documents(corpus_path)

        if not document_paths:
            print("❌ No documents found in corpus directory!")
            return

        # Step 2: Process documents
        documents = self.process_documents(document_paths)

        if not documents:
            print("❌ No documents were successfully processed!")
            return

        # Step 3: Chunk documents
        chunks = self.chunk_documents(documents)

        if not chunks:
            print("❌ No chunks were created!")
            return

        # Step 4: Ingest to Pinecone
        self.ingest_to_pinecone(chunks)

        print("\n✅ Ingestion pipeline completed successfully!")


def main():
    """Main entry point for the ingestion script."""
    parser = argparse.ArgumentParser(description="Ingest AI Pocket Projects corpus into Pinecone")
    parser.add_argument("--corpus - path", type=str, help="Path to the corpus directory (overrides config)")
    parser.add_argument("--clean", action="store_true", help="Clean the index before ingestion")

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print("❌ Configuration error: {e}")
        print("Please ensure pyproject.toml exists and set required environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - PINECONE_API_KEY")
        print("  - PINECONE_ENVIRONMENT")
        sys.exit(1)

    # Resolve corpus path
    corpus_path_str = args.corpus_path or config.corpus_path
    corpus_path = Path(corpus_path_str).resolve()
    if not corpus_path.exists():
        print("❌ Corpus directory not found: {corpus_path}")
        sys.exit(1)

    # Run ingestion
    ingester = CorpusIngester(config)
    ingester.run_ingestion(corpus_path, clean_index=args.clean)


if __name__ == "__main__":
    main()
