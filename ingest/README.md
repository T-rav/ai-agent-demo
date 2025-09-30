# AI Agent Demo - Document Ingestion System

This directory contains a Python-based ingestion system that processes the AI Pocket Projects corpus and stores it in Pinecone for semantic search capabilities.

## Features

- **Multi-format Support**: Processes PDF, Markdown, and text files with format-specific handling
- **Smart Chunking**: Advanced structure-aware chunking that respects document organization
- **Document Title Extraction**: Automatically extracts and stores document titles from various formats
- **Enhanced Metadata**: Rich metadata including titles, sections, page numbers, and structure info
- **OpenAI Embeddings**: Uses `text-embedding-3-small` model (1536 dimensions)
- **Pinecone Integration**: Stores vectors in Pinecone for fast similarity search with comprehensive metadata
- **Batch Processing**: Efficient batch processing for large document sets
- **Query Testing**: Built-in tools for testing search functionality with detailed result display

## Requirements

- **Python 3.11+** - This project requires Python 3.11 or higher
- **API Keys** - OpenAI and Pinecone API keys

## Setup

### 1. Install the Package

```bash
cd ingest
pip install -e .
```

This will install all dependencies and make the ingestion commands available.

### 2. Configure Environment Variables

**Option A: Using .env file (Recommended)**

Copy the example environment file and fill in your API keys:

```bash
cp env.example .env
```

Then edit `.env` with your actual values:
```bash
# Edit the .env file with your API keys
OPENAI_API_KEY=sk-your-actual-openai-key-here
PINECONE_API_KEY=your-actual-pinecone-key-here
PINECONE_ENVIRONMENT=your-pinecone-environment-here
```

**Option B: Export environment variables**

Set the required environment variables directly:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
export PINECONE_API_KEY=your_pinecone_api_key_here
export PINECONE_ENVIRONMENT=your_pinecone_environment_here
```

Or add them to your shell profile (`.bashrc`, `.zshrc`, etc.) for persistence:

```bash
echo 'export OPENAI_API_KEY=your_openai_api_key_here' >> ~/.zshrc
echo 'export PINECONE_API_KEY=your_pinecone_api_key_here' >> ~/.zshrc
echo 'export PINECONE_ENVIRONMENT=your_pinecone_environment_here' >> ~/.zshrc
source ~/.zshrc
```

### 3. Get API Keys

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Pinecone**: Sign up at [Pinecone](https://www.pinecone.io/) and get your API key

### 4. Validate Setup

Run the setup validation script to ensure everything is configured correctly:

```bash
python setup.py
# or use the installed command:
setup-ingest
```

## Usage

### Ingest Documents

Run the main ingestion script to process all documents in the corpus:

```bash
python ingest.py
# or use the installed command:
ingest-corpus
```

Options:
- `--corpus-path`: Path to corpus directory (overrides config)
- `--clean`: Clean the index before ingestion

Example with custom path:
```bash
python ingest.py --corpus-path /path/to/your/corpus --clean
# or:
ingest-corpus --corpus-path /path/to/your/corpus --clean
```

### Test Queries

After ingestion, test the search functionality:

```bash
# Interactive mode
python query_test.py --interactive
# or:
query-corpus --interactive

# Single query
python query_test.py --query "What is artificial intelligence?"
# or:
query-corpus --query "What is artificial intelligence?"

# Run sample queries
python query_test.py --sample-queries
# or:
query-corpus --sample-queries
```

## Architecture

### Document Processing Pipeline

1. **Discovery**: Finds all supported files (PDF, MD, TXT) in the corpus
2. **Processing**: Extracts text content and document titles from each document
3. **Smart Chunking**: Intelligently splits documents using structure-aware strategies:
   - **Markdown**: Respects headers and sections
   - **PDF**: Maintains page boundaries and structure
   - **Text**: Uses paragraph and sentence boundaries
4. **Embedding**: Generates embeddings using OpenAI's model
5. **Storage**: Stores vectors in Pinecone with comprehensive metadata

### File Structure

```
ingest/
├── README.md              # This file
├── pyproject.toml         # Python project configuration and dependencies
├── env.example           # Environment variables template
├── config_loader.py       # Configuration management
├── ingest.py             # Main ingestion script
├── document_processor.py # Document processing utilities
├── pinecone_client.py    # Pinecone vector store client
├── query_test.py         # Query testing utilities
└── setup.py              # Setup validation script
```

### Key Components

#### DocumentProcessor
- Handles PDF, Markdown, and text file processing with format-specific strategies
- Extracts clean text content and document titles
- Provides token counting and text normalization
- Smart title extraction from headers, filenames, and content patterns

#### SmartTextChunker
- Advanced structure-aware chunking system
- **Markdown**: Preserves section hierarchy and headers
- **PDF**: Maintains page boundaries and academic paper structure
- **Text**: Uses semantic paragraph and sentence boundaries
- Enhanced metadata with titles, sections, and page numbers
- Maintains context with intelligent overlapping chunks

#### PineconeVectorStore
- Manages Pinecone index operations
- Handles batch embedding generation
- Provides similarity search functionality

## Configuration

The system uses `pyproject.toml` for configuration with environment variable overrides. All configuration is defined in the `[tool.ai-agent-demo]` section.

### Environment Variables (Required)

- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key  
- `PINECONE_ENVIRONMENT`: Your Pinecone environment

### Configuration Sections in pyproject.toml

#### `[tool.ai-agent-demo.database]`
- `index_name`: Name of your Pinecone index (default: "ai-agent-demo-index")

#### `[tool.ai-agent-demo.embedding]`
- `model`: OpenAI embedding model (default: "text-embedding-3-small")
- `dimensions`: Vector dimensions (default: 1536)

#### `[tool.ai-agent-demo.processing]`
- `chunk_size`: Maximum tokens per chunk (default: 1000)
- `chunk_overlap`: Overlapping tokens between chunks (default: 200)
- `embedding_batch_size`: Batch size for embedding generation (default: 100)
- `upsert_batch_size`: Batch size for vector upserts (default: 100)

#### `[tool.ai-agent-demo.paths]`
- `corpus_path`: Path to corpus directory (default: "data/corpus")

#### `[tool.ai-agent-demo.logging]`
- `level`: Logging level (default: "INFO")
- `show_progress`: Show progress bars (default: true)

## Corpus Structure

The system processes the AI Pocket Projects corpus with the following structure:

```
ingest/data/corpus/
├── ai/                   # AI-related documents
│   ├── *.pdf            # Research papers
│   ├── *.md             # Concept explanations
│   └── ...
└── computing/           # Computing history documents
    ├── *.pdf            # Historical papers
    ├── *.md             # Timeline articles
    └── ...
```

## Troubleshooting

### Common Issues

1. **Python Version**: Ensure you're using Python 3.11 or higher
2. **Missing API Keys**: Ensure all required environment variables are set
3. **Index Not Found**: The script will create the index automatically
4. **Embedding Errors**: Check your OpenAI API key and quota
5. **Memory Issues**: Reduce batch sizes in pyproject.toml configuration
6. **Import Errors**: Run `pip install -e .` to install the package in development mode

### Debugging

Enable verbose logging by setting:
```bash
export LOG_LEVEL=DEBUG
python ingest.py
```

### Index Management

To reset your index:
```bash
python ingest.py --clean
# or:
ingest-corpus --clean
```

To check index statistics:
```bash
python query_test.py --sample-queries
# or:
query-corpus --sample-queries
```

## Performance Notes

- **Processing Time**: Depends on corpus size and API rate limits
- **Embedding Cost**: ~$0.02 per 1M tokens with text-embedding-3-small
- **Storage**: Each 1536-dim vector uses ~6KB in Pinecone
- **Query Speed**: Sub-second response times for similarity search

## Next Steps

After successful ingestion, you can:

1. **Integrate with Chat**: Connect to the UI for conversational search
2. **Add More Sources**: Expand the corpus with additional documents
3. **Tune Parameters**: Optimize chunking and embedding settings
4. **Monitor Usage**: Track query patterns and performance

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error logs for specific issues
3. Ensure all dependencies are correctly installed
4. Verify API keys and permissions
