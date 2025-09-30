#!/usr/bin/env python3
"""
Clean script for clearing the Pinecone vector index.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports when running directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from ..services import PineconeVectorStore  # noqa: E402
from .config_loader import load_config  # noqa: E402


def main():
    """Clean the Pinecone vector index."""
    try:
        # Load configuration
        config = load_config()

        # Initialize vector store
        vector_store = PineconeVectorStore(
            api_key=config.pinecone_api_key,
            environment=config.pinecone_environment,
            index_name=config.index_name,
            embedding_model=config.model,
            embedding_dimensions=config.dimensions,
        )

        # Connect to existing index and clear vectors
        try:
            vector_store.index = vector_store.pc.Index(vector_store.index_name)
            vector_store.delete_all_vectors()
            print("✅ Index cleaned successfully!")
        except Exception as e:
            print(f"❌ Could not clean index: {e}")
            print("The index may not exist or may be inaccessible.")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Please ensure pyproject.toml exists and set required environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - PINECONE_API_KEY")
        print("  - PINECONE_ENVIRONMENT")
        sys.exit(1)


if __name__ == "__main__":
    main()
