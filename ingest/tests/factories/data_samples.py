"""
Sample test data for various scenarios.
"""


class TestDataSamples:
    """Sample test data for various scenarios."""

    # Environment variable sets
    BASIC_ENV_VARS = {
        "OPENAI_API_KEY": "test - openai - key",
        "PINECONE_API_KEY": "test - pinecone - key",
        "PINECONE_ENVIRONMENT": "test - env",
    }

    EXTENDED_ENV_VARS = {
        **BASIC_ENV_VARS,
        "DATABASE_INDEX_NAME": "test - index",
        "EMBEDDING_MODEL": "text - embedding - 3-large",
        "EMBEDDING_DIMENSIONS": "3072",
        "CHUNK_SIZE": "1500",
        "CHUNK_OVERLAP": "300",
    }

    EMPTY_ENV_VARS = {"OPENAI_API_KEY": "", "PINECONE_API_KEY": "", "PINECONE_ENVIRONMENT": ""}

    # TOML configuration content
    SAMPLE_TOML_CONFIG = """
[tool.ai - agent - demo.api]
openai_api_key = ""
pinecone_api_key = ""
pinecone_environment = ""

[tool.ai - agent - demo.database]
index_name = "test - index - from - toml"

[tool.ai - agent - demo.embedding]
model = "text - embedding - 3-small"
dimensions = 1536

[tool.ai - agent - demo.processing]
chunk_size = 800
chunk_overlap = 150
min_chunk_size = 50
max_chunk_size = 1200

[tool.ai - agent - demo.paths]
corpus_path = "test / corpus"

[tool.ai - agent - demo.logging]
level = "DEBUG"
show_progress = false
"""

    # .env file content
    SAMPLE_ENV_CONTENT = """
OPENAI_API_KEY=dotenv - openai - key
PINECONE_API_KEY=dotenv - pinecone - key
PINECONE_ENVIRONMENT=dotenv - env
CHUNK_SIZE=2000
"""

    # Invalid TOML content
    INVALID_TOML_CONTENT = "invalid toml content ["
