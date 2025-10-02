# API Test Suite

Tests organized by concept following the ingest system patterns.

## Structure

```
tests/
├── api/                    # API endpoint tests
│   └── test_endpoints.py   # FastAPI endpoint tests organized by functionality
├── config/                 # Configuration tests
│   └── test_config.py      # Settings and environment variable tests
├── models/                 # Pydantic model tests
│   └── test_models.py      # Model validation tests
├── services/               # Service layer tests
│   ├── test_tools_service.py        # Agent tools tests
│   └── test_vector_store_service.py # Vector store tests
├── builders/               # Test data builders (fluent interface)
│   ├── request_builder.py  # Build ChatRequest, ChatMessage
│   └── response_builder.py # Build ChatResponse, SourceDocument, StreamChunk
├── factories/              # Test double factories
│   ├── agent_factory.py        # Create mock agents
│   ├── llm_factory.py          # Create mock LLMs
│   └── vector_store_factory.py # Create mock vector stores
└── conftest.py             # Minimal fixtures (env vars only)
```

## Patterns

### Builders (Fluent Interface)
Use builders to create test data with a fluent interface:

```python
from tests.builders import a_chat_request, a_chat_message

# Simple request
request = a_chat_request().build()

# Request with custom data
request = (
    a_chat_request()
    .with_message("Custom message")
    .with_session_id("session-123")
    .with_research_mode(True)
    .build()
)

# Request with history
request = (
    a_chat_request()
    .with_simple_history()
    .build()
)
```

### Factories (Test Doubles)
Use factories to create mocks and test doubles:

```python
from tests.factories import AgentFactory, VectorStoreFactory

# In your test
def test_something():
    mock_agent = AgentFactory.create_mock_agent()
    mock_vector_store = VectorStoreFactory.create_mock_vector_store()

    # Use mocks in test
    with patch("module.agent", mock_agent):
        # Test code
```

### NO Fixture Wrappers
❌ **Don't** wrap factories in fixtures:
```python
@pytest.fixture
def mock_agent():
    return AgentFactory.create_mock_agent()  # Redundant!
```

✅ **Do** use factories directly in tests:
```python
def test_something():
    mock_agent = AgentFactory.create_mock_agent()  # Direct usage
```

## Test Organization

### By Concept, Not By File
Tests are grouped by what they test:

- **API Tests** (`api/`) - Test HTTP endpoints, request/response handling
- **Config Tests** (`config/`) - Test configuration and settings
- **Model Tests** (`models/`) - Test Pydantic models and validation
- **Service Tests** (`services/`) - Test business logic and external services

### Class-Based Organization
Tests within files are organized into classes by functionality:

```python
class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root_endpoint(self):
        ...

    def test_health_endpoint(self):
        ...

class TestChatEndpoints:
    """Tests for chat endpoints."""

    def test_chat_endpoint(self):
        ...
```

## Running Tests

```bash
# All tests with coverage
make test

# Specific test file
pytest tests/api/test_endpoints.py -v

# Specific test class
pytest tests/api/test_endpoints.py::TestChatEndpoints -v

# Specific test
pytest tests/api/test_endpoints.py::TestChatEndpoints::test_chat_endpoint -v

# With coverage
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=70
```

## Coverage Target

- **Minimum**: 70%
- **Current**: ~67% (needs improvement)
- **Goal**: 75%+

## Best Practices

1. **Use builders for test data** - Makes tests readable and maintainable
2. **Use factories for mocks** - Consistent test doubles across tests
3. **Test by concept** - Group related tests together
4. **Class-based organization** - Clear test structure
5. **Descriptive test names** - Test names should describe what they test
6. **Minimal fixtures** - Only fixture what's truly shared and complex
