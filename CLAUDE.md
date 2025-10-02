# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a production-ready AI assistant with intelligent routing, RAG with source citations, and a React TypeScript frontend. The system uses **LangGraph** for multi-agent orchestration with two distinct workflows:

1. **Simple RAG**: Fast queries with automatic knowledge base retrieval
2. **Research Mode**: Multi-agent system (Planner → Gatherer → Report Builder) for comprehensive research

**Tech Stack**: React, TypeScript, FastAPI, LangGraph, OpenAI GPT-4, Pinecone, Tavily

## Architecture

### High-Level Flow

```
User Request → Router (GPT-3.5) → Decision (SIMPLE vs RESEARCH)
│
├─ SIMPLE: Automatic RAG → Simple Agent → Response with citations
│
└─ RESEARCH: Research Planner → Research Gatherer (loops) → Report Builder
```

### Key Components

**API (Python/FastAPI)**:
- `agent.py` - LangGraph workflow orchestration (router, agents, state management)
- `tools.py` - Tool definitions (KB search, web search, planning, report building)
- `vector_store.py` - Pinecone vector store service
- `main.py` - FastAPI endpoints with SSE streaming
- `config.py` - Configuration management

**UI (React/TypeScript)**:
- `src/components/ChatContainer/` - Main chat interface
- `src/hooks/useChat.ts` - Chat state management and streaming
- `src/services/chatService.ts` - API communication with SSE support

**Ingest (Python)**:
- `ingest/core/ingest.py` - Document ingestion pipeline
- `ingest/services/chunker.py` - Document chunking strategy
- `ingest/services/embedder.py` - OpenAI embeddings

### Multi-Agent Orchestration

The system uses **dedicated agents** for different phases:

1. **Router Node**: Classifies intent (GPT-3.5-turbo for speed/cost)
2. **Simple RAG Node**: Automatic Pinecone retrieval (no agent choice)
3. **Simple Agent**: Answers with citations from RAG context
4. **Research Planner Agent**: Breaks down topics into subtopics
5. **Research Gatherer Agent**: Searches KB and web, collects sources (loops until complete)
6. **Report Builder Agent**: Synthesizes findings into markdown report with citations

Each agent has **isolated tool access** and clear phase boundaries. See `docs/ARCHITECTURE.md` for detailed workflow diagrams.

### State Management

```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sources: List[dict]
    routing_decision: str  # "simple" or "research"
```

State flows through nodes, accumulating messages and sources. LangSmith traces every node transition.

## Development Commands

### Running the Application

```bash
# Start all services (UI + API via Docker)
make start

# Start individual services
make ui    # Frontend only
make api   # Backend only

# View logs
make logs

# Stop all services
make stop
```

**Ports**:
- UI: http://localhost:3000
- API: http://localhost:8000

### Testing

**Run all tests**:
```bash
make test           # All tests (UI + API in Docker)
make test-ui        # UI tests only
make test-api       # API tests only
cd ingest && make test  # Ingest tests (requires local Python 3.11+)
```

**Run single test**:
```bash
# API (from api/)
python -m pytest tests/services/test_agent_service.py::TestRAGAgentInitialization::test_creates_graph -v

# UI (from ui/)
npm test -- ChatContainer.test.tsx
```

**Test requirements**:
- **API**: 70% coverage minimum (all metrics)
- **Ingest**: 70% coverage minimum (all metrics)
- **UI**: 70% coverage minimum (60% for branches due to React edge cases)
- All API tests must use `--cache-clear` to avoid pytest caching issues

### Code Quality

```bash
# Format code
make format         # All services
make format-ui      # UI only (Prettier)
make format-api     # API only (Black + isort)

# Lint
make lint           # All services
make lint-ui        # ESLint
make lint-api       # flake8 + bandit

# Check formatting without changes
make format-check
make format-check-ui

# TypeScript compilation check
make check

# Run full CI pipeline
make ci             # format-check + lint + test for all services
```

### Ingest System

```bash
cd ingest

# One-time setup (first run)
make dev-install    # Install dependencies
make run            # Ingest documents from data/corpus/

# Maintenance
make run-fresh      # Clean index and re-ingest
make run-clean      # Remove all vectors
make query          # Interactive query tool
```

## Test Architecture

### Test Patterns

This codebase follows the **Humaid Principle** for test factories:

**✅ Good** - Pass configuration to factory:
```python
mock_llm = LLMFactory.create_mock_llm(response_content="Custom response")
mock_router = LLMFactory.create_mock_router_llm(decision="RESEARCH")
```

**❌ Bad** - Setting properties after creation:
```python
mock = MagicMock()
mock.ainvoke = AsyncMock(return_value=...)  # Don't do this!
```

### Test Structure

**API Tests** (`api/tests/`):
- `conftest.py` - Configures `sys.path` for absolute imports
- `factories/` - Centralized mock creation (VectorStoreFactory, LLMFactory, ConfigFactory)
- `builders/` - Request builders for API testing
- Test isolation: Imports are patched at module level to prevent caching issues

**UI Tests** (`ui/src/`):
- `test-utils/factories/` - Data factories (MessageFactory)
- `test-utils/builders/` - Fluent builders (MessageBuilder)
- `test-utils/mockData.ts` - Shared mock data

### Common Test Issues

1. **Test isolation failures**: If tests pass individually but fail in suite, check for module-level imports being cached. Solution: Import inside patch context and ensure `sys.path` is configured in `conftest.py`.

2. **Coverage drops**: Tests/utilities are included in coverage. Prefer adding tests over excluding files from coverage.

3. **Flaky UI tests**: Add explicit timeouts to `waitFor()` calls (3000ms recommended for CI).

## Code Formatting Rules

- **Python**: Black (line-length=100), isort (profile="black")
- **TypeScript**: Prettier (default config)
- **Imports**: Absolute imports preferred (`from tests.factories import ...`)
- **Pre-commit hooks**: Run automatically via git hooks (trim whitespace, check yaml, format, lint)

## Configuration

**Environment Variables** (required):
- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone API key
- `PINECONE_ENVIRONMENT` - Pinecone environment
- `TAVILY_API_KEY` - Tavily API key (optional, for web search)

**Setup**:
```bash
cp api/env.example api/.env
cp ingest/env.example ingest/.env
# Edit both .env files with your API keys
```

## Common Workflows

### Adding a New Agent

1. Define agent function in `api/agent.py` (follow pattern: `_agent_name(state: AgentState) -> dict`)
2. Add tools to `api/tools.py` if needed
3. Add node to workflow: `workflow.add_node("agent_name", _agent_name)`
4. Add edges/conditional edges for routing
5. Create tests in `api/tests/services/test_agent_service.py`
6. Use factories from `api/tests/factories/` for mocks

### Adding a New Tool

1. Define tool function in `api/tools.py` with `@tool` decorator
2. Add to appropriate tools list (simple_tools, research_tools)
3. Document in tool docstring (agents read this!)
4. Test in `api/tests/services/test_tools.py`

### Debugging Agent Workflow

1. Check LangSmith traces (https://smith.langchain.com/)
2. Enable verbose logging in `api/agent.py`
3. Check routing decision in state: `state["routing_decision"]`
4. Inspect tool calls in messages: `last_message.tool_calls`

## Important Notes

- **LangGraph State**: Use `add_messages` reducer to accumulate messages, not replace them
- **Citation Format**: Simple mode uses `Source 1`, Research mode uses `[KB-1]` and `[WEB-1]`
- **Router Speed**: Uses GPT-3.5-turbo for cost/speed, other agents use GPT-4
- **Test Isolation**: Always run API tests with `--cache-clear` flag
- **Docker Development**: All services run in Docker by default for consistency
- **Coverage Threshold**: 70% minimum enforced in CI (UI branches at 60% due to React edge cases)

## Documentation

- **Architecture**: `docs/ARCHITECTURE.md` - Detailed workflow diagrams and agent descriptions
- **API README**: `api/README.md` - API-specific documentation
- **Ingest README**: `ingest/README.md` - Ingestion system documentation
- **Main README**: `README.md` - Quick start and usage examples
