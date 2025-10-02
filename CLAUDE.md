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

## Engineering Principles

### Testing Philosophy

**Organize by Concept, Not Structure**

Tests should mirror what you're verifying, not the file system. Group related behaviors together:
- Group tests by feature area or user journey, not by implementation file
- Use class-based test organization to cluster related scenarios
- Name tests to describe behavior: `test_rejects_invalid_email` not `test_validation_method_1`

**The Builder-Factory Pattern**

Separate test data creation from test logic:
- **Builders**: Create domain objects with fluent interfaces (`a_user().with_email("...").build()`)
- **Factories**: Create test doubles (mocks, stubs) with pre-configured behavior
- Pass configuration to factories at creation time, never mutate after construction
- This pattern eliminates brittle test setup and makes tests self-documenting

**Avoid Fixture Overuse**

Fixtures create hidden dependencies and coupling:
- Only use fixtures for truly shared, complex setup (like database connections)
- Prefer direct builder/factory calls in tests for clarity
- If you find yourself wrapping a factory in a fixture, remove the fixture

**Coverage as a Conversation Starter**

Coverage metrics tell you what code is executed, not what behaviors are verified:
- 70% minimum is a floor, not a ceiling
- Missing coverage often reveals untested edge cases or dead code
- 100% coverage doesn't mean bug-free; it means your tests ran all lines at least once
- Focus on testing critical paths thoroughly over hitting arbitrary numbers

### Observability and Tracing

**Visibility Before Debugging**

Every system behavior should be observable without code changes:
- Instrument decision points: what path did the system take and why?
- Capture inputs and outputs at boundaries (API calls, tool executions, agent decisions)
- Track latency at each stage to identify bottlenecks
- Log errors with enough context to understand what the system was attempting

**Structured Over Unstructured**

Logs should be queryable, not just readable:
- Use structured formats that machines can parse and aggregate
- Include correlation IDs to trace requests across services
- Tag events with dimensions (user_id, session_id, decision_type) for filtering
- Avoid logging sensitive data; use redaction if necessary

**Trace Complete User Journeys**

A single user action often triggers multiple system operations:
- Connect related events with trace IDs so you can follow the full story
- Capture timing data to understand where time is spent
- Show state transitions to understand how data changes through the pipeline
- Make traces accessible to engineers without database access

**Health Checks and Readiness**

Systems should self-report their health:
- Distinguish between "alive" (process is running) and "ready" (can handle traffic)
- Check dependencies in health endpoints (can we reach the database? the API?)
- Make health checks lightweight; they'll be called frequently
- Use health data to automatically route traffic away from degraded instances

### Security

**Defense in Depth**

Never rely on a single security control:
- Validate input at every boundary (UI, API, database)
- Assume every external input is malicious until proven otherwise
- Use allowlists (known good) over denylists (known bad) when possible
- Apply the principle of least privilege: grant minimum necessary permissions

**Secrets Management**

Credentials should never live in code:
- Use environment variables or secret management services
- Rotate secrets regularly; treat rotation as a normal operation
- Never log secrets, even in debug mode
- Use different credentials for different environments

**Authentication vs Authorization**

Know who they are (authentication) and what they can do (authorization):
- Verify identity before granting access (don't trust client-supplied identity)
- Check permissions at the resource level, not just the endpoint level
- Default to deny; require explicit grants
- Audit authorization failures to detect attack attempts

**Network Security**

Control what can communicate with what:
- Restrict cross-origin requests to known clients
- Use encryption in transit (TLS) for all external communication
- Validate all external inputs before processing
- Rate limit to prevent abuse and resource exhaustion

**Update Dependencies Regularly**

Today's secure library is tomorrow's vulnerability:
- Monitor for security advisories in your dependencies
- Update promptly when vulnerabilities are disclosed
- Pin versions to avoid surprise breaking changes
- Balance stability with security; sometimes you must take the update

### Code Organization

**Single Concept Per File**

Each file should answer one question:
- **Models**: What data structures exist? (`user.py`, `chat_message.py`)
- **Services**: What business operations can we perform? (`vector_store.py`, `document_processor_service.py`)
- **Configuration**: How is the system configured? (`config.py`)
- **Tools**: What capabilities do we expose? (`tools.py`)

This makes files findable: need the User model? Look in `user.py`, not `models/business/entities/user.py`.

**Avoid Deep Nesting**

Depth creates navigation burden:
- Prefer flat structures: `services/email_service.py` over `services/communication/email/email_service.py`
- If you need categories, use one level: `models/user.py`, `models/message.py`
- Deep nesting often signals missing abstractions or overly complex organization
- Exception: group tests by concept (`tests/services/`, `tests/models/`) to separate test code from production code

**Co-locate Related Concerns**

Files that change together should live together:
- Put all chat-related models in `models/` (message, request, response)
- Put all agent-related logic in one place (`agent.py`)
- Don't scatter a feature across distant directories
- If you're frequently jumping between files, consider merging them

**Explicit Over Implicit**

Code should reveal intent:
- Use descriptive names: `retry_with_exponential_backoff()` not `retry()`
- Make dependencies explicit through imports and type hints
- Avoid magic: globals, implicit side effects, hidden state
- Configuration should be declarative and centralized, not scattered

**Small, Focused Modules**

A file should fit in your head:
- If a file is hard to navigate, split it by responsibility
- Each module should have a clear purpose expressible in one sentence
- Large files often mean multiple concepts bundled together
- Size isn't the only metric; a 500-line file with one concept is fine

## Documentation

- **Architecture**: `docs/ARCHITECTURE.md` - Detailed workflow diagrams and agent descriptions
- **API README**: `api/README.md` - API-specific documentation
- **Ingest README**: `ingest/README.md` - Ingestion system documentation
- **Main README**: `README.md` - Quick start and usage examples
