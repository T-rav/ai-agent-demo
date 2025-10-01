# AI Deep Research Assistant

An intelligent research agent that writes comprehensive reports on AI and Computing topics, built with LangChain, LangGraph, and LangSmith.

## What It Does

This is not just a chatbot - it's an **autonomous research agent** that:

1. **Plans Research**: Breaks down complex topics into subtopics and research questions
2. **Gathers Information**: Searches knowledge base (established concepts) AND web (latest info)
3. **Synthesizes Findings**: Combines information from multiple sources
4. **Writes Reports**: Generates structured, comprehensive reports with citations
5. **Cites Sources**: Transparently shows where information comes from

## Features

- **Deep Research Mode**: Multi-step research workflow with LangGraph orchestration
- **Dual Knowledge Sources**: RAG system (Pinecone) + Web Search (Tavily)
- **Intelligent Planning**: Agent autonomously plans research approach
- **Report Generation**: Structured reports with sections, citations, and analysis
- **Observability**: LangSmith tracing shows every research step
- **Streaming**: Watch the research happen in real-time

## Architecture

### LangChain
Used for:
- LLM integration (OpenAI)
- Vector store operations (Pinecone)
- Embeddings generation
- Tool definitions

### LangGraph
Provides the agent workflow orchestration:
- **Agent Node**: Decides which tools to use based on the user query
- **Tool Node**: Executes selected tools (knowledge base search, web search)
- **Conditional Edges**: Routes between agent and tools until a final answer is generated

### LangSmith
Enables observability:
- Traces all LLM calls
- Monitors tool executions
- Debug agent decision-making
- Track performance metrics

## Setup

1. **Install dependencies**:
```bash
cd api/
pip install -e .
```

2. **Configure environment** (IMPORTANT!):
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

See **`ENV_SETUP.md`** for detailed instructions on getting each API key!

3. **Required API Keys**:
- ✅ `OPENAI_API_KEY`: For LLM and embeddings - **GET IT**: https://platform.openai.com/api-keys
- ✅ `PINECONE_API_KEY`: For vector store - **GET IT**: https://app.pinecone.io/
- ✅ `PINECONE_ENVIRONMENT`: Your Pinecone region (e.g., us-east-1-aws)
- ✅ `PINECONE_INDEX_NAME`: Must match your ingested index name!

4. **Optional API Keys** (Highly Recommended):
- 🌐 `TAVILY_API_KEY`: Enables web search - **GET IT**: https://app.tavily.com/
- 📊 `LANGCHAIN_API_KEY`: Enables observability - **GET IT**: https://smith.langchain.com/
- 📊 `LANGCHAIN_TRACING_V2`: Set to `true` to enable tracing

5. **Verify Setup**:
```bash
uvicorn main:app --reload
# Visit http://localhost:8000/ - should show features enabled
```

## Running the API

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker
```bash
docker build -t ai-agent-api .
docker run -p 8000:8000 --env-file .env ai-agent-api
```

## API Endpoints

### `GET /`
Health check and feature status

### `GET /health`
Simple health check

### `POST /api/chat`
Non-streaming chat endpoint

**Simple Question**:
```json
{
  "message": "What is LangChain?",
  "conversation_history": []
}
```

**Research Request**:
```json
{
  "message": "Write a comprehensive report on RAG systems",
  "research_mode": true
}
```

Response:
```json
{
  "message": "# Comprehensive Report on RAG Systems\n\n## Executive Summary...",
  "sources": [
    {
      "content": "...",
      "metadata": {"source": "rag_intro.md", "title": "What is RAG?"},
      "score": 0.95
    }
  ],
  "research_steps": [
    "Planning research approach",
    "Searching knowledge base",
    "Searching web",
    "Creating report outline",
    "Writing report"
  ]
}
```

### `POST /api/chat/stream`
Streaming chat endpoint with Server-Sent Events

Request: Same as `/api/chat`

Response: SSE stream with chunks:
```json
{"type": "token", "content": "LangChain"}
{"type": "token", "content": " is"}
{"type": "sources", "sources": [...]}
{"type": "done"}
```

## How It Works

### Simple Questions
1. User asks a quick question
2. Agent searches knowledge base or web
3. Returns concise answer with sources

### Research Reports (The Agentic Part!)
1. **PLAN**: Agent uses `research_topic_breakdown` to create research strategy
2. **GATHER**: Agent autonomously searches both:
   - Knowledge base (Pinecone) for foundational concepts
   - Web (Tavily) for latest information
3. **SYNTHESIZE**: Agent combines information from multiple sources
4. **STRUCTURE**: Agent creates report outline
5. **WRITE**: Agent generates comprehensive report with citations
6. **STREAM**: User watches research happen in real-time

**This is true agentic behavior**: The agent decides when to use which tools, makes multiple tool calls, and orchestrates a complex multi-step workflow.

## Agent Workflow

### LangGraph State Machine

```
User: "Write a comprehensive report on RAG systems"
    ↓
┌────────────────────────────────┐
│  Agent Node (LLM)              │
│  Decision: Use topic breakdown │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Tool Node                     │
│  Execute: research_topic_breakdown │
│  Returns: Research plan        │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Agent Node (LLM)              │
│  Decision: Search KB for       │
│            RAG fundamentals    │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Tool Node                     │
│  Execute: search_knowledge_base│
│  Returns: 5 sources on RAG     │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Agent Node (LLM)              │
│  Decision: Search web for      │
│            latest RAG research │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Tool Node                     │
│  Execute: tavily_search        │
│  Returns: Recent articles      │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Agent Node (LLM)              │
│  Decision: Create outline      │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Tool Node                     │
│  Execute: create_report_outline│
│  Returns: Report structure     │
└───────────┬────────────────────┘
            ↓
┌────────────────────────────────┐
│  Agent Node (LLM)              │
│  Decision: Generate report     │
│  Uses: All gathered sources    │
└───────────┬────────────────────┘
            ↓
    Comprehensive Report
    with Citations
```

**Key Point**: The agent makes multiple autonomous decisions about which tools to use and when, orchestrating a complex research workflow.

## LangSmith Observability

**100% of both flows are traced!** Every request is logged with complete visibility:

✅ **Router Decision**: See if it chose SIMPLE or RESEARCH mode
✅ **Agent Reasoning**: View which tools it decided to use
✅ **Tool Executions**: See inputs, outputs, and latency
✅ **Token Usage**: Monitor costs per request
✅ **Performance**: Track latency bottlenecks
✅ **Debugging**: Understand why decisions were made

See **`TRACING_GUIDE.md`** for detailed examples of what gets traced!

Access your traces at: https://smith.langchain.com

## Customization

### Adding New Tools
Add tools in `tools.py`:

```python
@tool
async def my_custom_tool(query: str) -> str:
    """Description of what the tool does."""
    # Tool implementation
    return result
```

### Adjusting Agent Behavior
Modify the system message in `agent.py` to change how the agent behaves.

### Vector Store Configuration
Update settings in `config.py` or environment variables:
- `RETRIEVAL_K`: Number of documents to retrieve
- `EMBEDDING_MODEL`: OpenAI embedding model to use

## Troubleshooting

### No results from knowledge base
- Ensure Pinecone index exists and has data
- Check if index name matches configuration
- Verify embeddings are generated correctly

### Web search not working
- Verify `TAVILY_API_KEY` is set
- Check Tavily API quota/limits

### LangSmith traces not appearing
- Verify `LANGCHAIN_TRACING_V2=true`
- Ensure `LANGCHAIN_API_KEY` is valid
- Check project name matches LangSmith dashboard

## Development

### Project Structure
```
api/
├── main.py              # FastAPI application
├── agent.py             # LangGraph agent workflow
├── tools.py             # Agent tools (KB search, web search)
├── vector_store.py      # Pinecone vector store service
├── models.py            # Pydantic models
├── config.py            # Configuration and settings
├── pyproject.toml       # Python project config & dependencies
└── README.md           # This file
```

### Testing
```bash
# Run tests (when implemented)
pytest

# Test endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is LangChain?"}'
```

## License

See LICENSE file in project root.
