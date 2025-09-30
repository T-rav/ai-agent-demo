#!/usr/bin/env python3
"""
Test script for querying the ingested corpus in Pinecone.
Allows testing search functionality and exploring the vector database.
"""

import argparse
import sys
from typing import Any, Dict, List

from ..models.exceptions import ConfigurationError
from ..services import PineconeVectorStore
from .config_loader import load_config


def print_search_results(results: List[Dict[str, Any]], query: str) -> None:
    """Print search results in a formatted way with enhanced metadata."""
    print(f"\n🔍 Search Results for: '{query}'")
    print("=" * 80)

    if not results:
        print("No results found.")
        return

    for i, result in enumerate(results, 1):
        score = result["score"]
        metadata = result["metadata"]

        print(f"\n{i}. 📊 Score: {score:.4f}")

        # Document information
        doc_title = metadata.get("document_title", "Unknown")
        file_name = metadata.get("file_name", "Unknown")
        print(f"   📄 Document: {doc_title}")
        if doc_title != file_name:
            print(f"   📁 File: {file_name}")

        # Structure information
        file_type = metadata.get("file_type", "Unknown")
        chunk_index = metadata.get("chunk_index", "Unknown")
        print(f"   📝 Type: {file_type} | Chunk: {chunk_index}")

        # Section / page information if available
        section_header = metadata.get("section_header")
        page_number = metadata.get("page_number")

        if section_header:
            print(f"   📑 Section: {section_header}")
        if page_number:
            print(f"   📖 Page: {page_number}")

        # Size information
        token_count = metadata.get("token_count", "Unknown")
        print(f"   🔢 Tokens: {token_count}")

        # Print content preview
        content_preview = metadata.get("content_preview", "")
        if content_preview:
            # Clean up the preview
            preview = content_preview.replace("\n", " ").strip()
            if len(preview) > 300:
                preview = preview[:300] + "..."
            print(f"   💬 Preview: {preview}")

        print("─" * 80)


def interactive_query_mode(vector_store: PineconeVectorStore) -> None:
    """Run interactive query mode for testing searches."""
    print("\n🎯 Interactive Query Mode")
    print("Type your queries to search the corpus. Type 'quit' to exit.")
    print("Commands:")
    print("  - 'stats' - Show index statistics")
    print("  - 'quit' - Exit interactive mode")
    print("-" * 50)

    while True:
        try:
            query = input("\nQuery: ").strip()

            if query.lower() in ["quit", "exit", "q"]:
                break
            elif query.lower() == "stats":
                stats = vector_store.get_index_stats()
                print("\n📊 Index Statistics:")
                for key, value in stats.items():
                    print(f"   {key}: {value}")
                continue
            elif not query:
                continue

            # Perform search
            results = vector_store.query_similar(query, top_k=5)
            print_search_results(results, query)

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def run_sample_queries(vector_store: PineconeVectorStore) -> None:
    """Run a set of sample queries to test the system."""
    sample_queries = [
        "What is artificial intelligence?",
        "How do transformers work in deep learning?",
        "What are the challenges with RAG systems?",
        "History of computing and early computers",
        "Machine learning algorithms and techniques",
        "Ethical considerations in AI development",
        "What is prompt engineering and how does it work?",
        "Deep learning neural networks architecture",
        "Attention mechanisms in language models",
        "Computer vision and image processing",
        "Natural language processing techniques",
    ]

    print("\n🧪 Running Sample Queries")
    print("=" * 50)

    for query in sample_queries:
        print(f"\nTesting query: '{query}'")
        try:
            results = vector_store.query_similar(query, top_k=3)
            if results:
                print(f"✅ Found {len(results)} results (top score: {results[0]['score']:.4f})")
                # Print just the top result details
                top_result = results[0]
                metadata = top_result["metadata"]
                print(
                    f"   Best match: {metadata.get('file_name', 'Unknown')} (chunk {metadata.get('chunk_index', 'Unknown')})"
                )
            else:
                print("❌ No results found")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main entry point for the query test script."""
    parser = argparse.ArgumentParser(description="Test queries against the ingested corpus")
    parser.add_argument("--query", type=str, help="Single query to test")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--sample-queries", action="store_true", help="Run sample queries for testing")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config()
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure pyproject.toml exists and set required environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - PINECONE_API_KEY")
        print("  - PINECONE_ENVIRONMENT")
        sys.exit(1)

    # Initialize vector store
    vector_store = PineconeVectorStore(
        api_key=config.pinecone_api_key,
        environment=config.pinecone_environment,
        index_name=config.index_name,
        embedding_model=config.model,
        embedding_dimensions=config.dimensions,
    )

    # Connect to existing index
    try:
        vector_store.index = vector_store.pc.Index(config.index_name)

        # Check if index has data
        stats = vector_store.get_index_stats()
        if stats["total_vector_count"] == 0:
            print("❌ Index is empty. Please run ingestion first.")
            sys.exit(1)

        print(f"✅ Connected to index '{config.index_name}'")
        print(f"   Total vectors: {stats['total_vector_count']}")
        print(f"   Dimensions: {stats['dimension']}")

    except Exception as e:
        print(f"❌ Error connecting to index: {str(e)}")
        sys.exit(1)

    # Run based on arguments
    if args.query:
        # Single query
        results = vector_store.query_similar(args.query, top_k=args.top_k)
        print_search_results(results, args.query)
    elif args.sample_queries:
        # Sample queries
        run_sample_queries(vector_store)
    elif args.interactive:
        # Interactive mode
        interactive_query_mode(vector_store)
    else:
        # Default: show stats and run interactive mode
        stats = vector_store.get_index_stats()
        print("📊 Index Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

        interactive_query_mode(vector_store)


if __name__ == "__main__":
    main()
