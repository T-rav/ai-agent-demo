# 🤖 AI Assistant Demo

![AI Assistant Demo](./docs/screenshot.png)

> A production-ready AI assistant with intelligent routing, RAG (Retrieval-Augmented Generation) with source citation, and a beautiful React TypeScript frontend.

This system features **automatic knowledge base search** for quick answers (95% of queries) and **multi-agent research workflows** for comprehensive reports (when explicitly requested). Built with LangGraph, FastAPI, and React.

---

## 🚀 Features

### 🤖 Intelligent Routing System
- ✅ **Smart Mode Detection**: Automatically routes to simple RAG or multi-agent research based on user intent
- ✅ **Simple Mode**: Quick answers with automatic knowledge base retrieval (95% of queries)
- ✅ **Research Mode**: Comprehensive multi-agent workflow for detailed reports (explicit requests only)
- ✅ **GPT-4o-mini Router**: Fast, accurate routing with clear instruction-following

### 🧠 Advanced RAG Pipeline
- ✅ **Vector Store Integration**: Pinecone-powered semantic search across knowledge base
- ✅ **Automatic Retrieval**: Simple queries automatically fetch relevant context
- ✅ **Source Citations**: All responses include source documents with relevance scores
- ✅ **Markdown Documents**: Supports ingestion of markdown and PDF documentation

### 🔬 Multi-Agent Research System
- ✅ **Research Planner**: Breaks down complex topics into research subtopics
- ✅ **Research Gatherer**: Collects information from knowledge base and web sources
- ✅ **Report Builder**: Synthesizes findings into comprehensive markdown reports
- ✅ **LangGraph Orchestration**: Sophisticated workflow management with state tracking

### 💬 Modern Frontend (React UI)
- ✅ **Beautiful Dark Theme**: Professional, modern interface with smooth animations
- ✅ **Real-time Streaming**: Token-by-token streaming for natural conversation flow
- ✅ **Mode Indicators**: Visual badges showing simple vs research mode
- ✅ **Source Display**: Expandable source citations with document titles and scores
- ✅ **Export to Markdown**: Download full conversations with sources and metadata
- ✅ **TypeScript**: Full type safety and excellent developer experience
- ✅ **Comprehensive Testing**: Full test coverage with Jest and React Testing Library
- ✅ **Mobile Responsive**: Works seamlessly on desktop and mobile devices

### ⚡ Backend (Python FastAPI)
- ✅ **FastAPI Framework**: High-performance async API with automatic OpenAPI docs
- ✅ **LangGraph Workflows**: Sophisticated agent orchestration and state management
- ✅ **Streaming Responses**: Server-Sent Events for real-time token streaming
- ✅ **Web Search Integration**: Tavily API for current information and trends
- ✅ **OpenAI Integration**: GPT-4 for responses, GPT-4o-mini for routing
- ✅ **Docker Ready**: Production and development Docker configurations

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework with hooks
- **TypeScript** - Type safety and better DX
- **CSS3** - Custom styling with dark theme
- **Jest & React Testing Library** - Comprehensive test coverage
- **Server-Sent Events** - Real-time streaming

### Backend
- **Python 3.11** - Modern Python with type hints
- **FastAPI** - High-performance async web framework
- **LangChain** - LLM orchestration and tooling
- **LangGraph** - Multi-agent workflow management
- **OpenAI GPT-4** - Main language model
- **OpenAI GPT-4o-mini** - Fast routing decisions
- **Pinecone** - Vector database for semantic search
- **Tavily** - Web search API
- **Pydantic** - Data validation and settings
- **Pytest** - Testing framework

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Production web server
- **Uvicorn** - ASGI server
- **Make** - Build automation

## 📁 Project Structure

```
ai-agent-demo/
├── api/                         # Python FastAPI backend
│   ├── agent.py                 # LangGraph RAG agent with routing
│   ├── main.py                  # FastAPI application
│   ├── tools.py                 # Knowledge base & web search tools
│   ├── vector_store.py          # Pinecone integration
│   ├── models/                  # Pydantic models
│   └── tests/                   # Backend test suite
├── ingest/                      # Document ingestion pipeline
│   ├── core/
│   │   ├── ingest.py            # Main ingestion script
│   │   └── setup.py             # Vector store setup
│   ├── data/corpus/             # Knowledge base documents
│   ├── models/                  # Data models
│   ├── services/                # Processing services
│   └── utils/                   # Utilities
├── ui/                          # React TypeScript frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ChatContainer/   # Main chat container
│   │   │   ├── MessageList/     # Message display with sources
│   │   │   ├── MessageInput/    # Message input
│   │   │   └── Message/         # Individual message
│   │   ├── hooks/               # Custom React hooks (useChat)
│   │   ├── services/            # API service (streaming)
│   │   ├── types/               # TypeScript definitions
│   │   └── test-utils/          # Testing utilities
│   ├── Dockerfile               # Production Docker config
│   └── Dockerfile.dev           # Development Docker config
├── docker-compose.yml           # Production compose
└── docker-compose.dev.yml       # Development compose
```

## 🎯 How It Works

### Simple Query Flow (95% of queries)
```
User: "How does AI support exploring Mars?"
  ↓
Router (GPT-4o-mini): Classifies as SIMPLE
  ↓
Simple RAG Node: Auto-queries Pinecone vector store
  ↓
Simple Agent: Generates answer with source citations
  ↓
Response: "AI supports exploring Mars in several key ways..."
```

### Research Query Flow (explicit requests)
```
User: "Write a comprehensive report on AI in healthcare"
  ↓
Router (GPT-4o-mini): Classifies as RESEARCH
  ↓
Research Planner: Breaks down into subtopics
  ↓
Research Gatherer: Searches KB + Web for each topic
  ↓
Report Builder: Synthesizes into structured markdown report
  ↓
Response: Comprehensive multi-section report with citations
```

## 🛠️ Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- OR: Node.js 18+, Python 3.11+
- OpenAI API key
- Pinecone API key
- Tavily API key (optional, for web search)

### 1. Environment Setup

Create `.env` files in both `api/` and `ingest/` directories:

```bash
# api/.env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=your_index
TAVILY_API_KEY=your_tavily_key  # optional
```

```bash
# ingest/.env
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENVIRONMENT=your_environment
PINECONE_INDEX_NAME=your_index
```

### 2. Ingest Knowledge Base

```bash
cd ingest
pip install -e .
python -m core.setup        # Create Pinecone index
python -m core.ingest       # Ingest documents from data/corpus/
```

### 3. Start Services

#### Using Docker Compose (Recommended)
```bash
docker-compose -f docker-compose.dev.yml up
```

#### Using Makefile
```bash
make install    # Install dependencies
make start      # Start all services
```

#### Manual Setup
```bash
# Terminal 1: Start API
cd api
pip install -e .
uvicorn main:app --reload --port 8000

# Terminal 2: Start UI
cd ui
npm install
npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Testing

### Frontend Tests
```bash
cd ui
npm test                    # Interactive mode
npm run test -- --coverage # With coverage report
```

### Backend Tests
```bash
cd api
pytest                      # Run all tests
pytest --cov                # With coverage
```

### Ingest Tests
```bash
cd ingest
pytest                      # Run all tests
pytest --cov                # With coverage
```

## 🎨 UI Features

### Chat Interface
- **Empty State**: Welcoming message when no conversation exists
- **Message Display**: User and assistant messages with timestamps and mode badges
- **Source Citations**: Expandable source panels showing document titles, files, and relevance scores
- **Streaming Responses**: Real-time token-by-token display as AI generates responses
- **Export Chat**: Download full conversation history as markdown with sources
- **Clear Conversation**: Option to clear chat history
- **Error Handling**: User-friendly error messages with dismiss option

### Design System
- **Dark Theme**: Professional dark mode with green accent colors
- **Typography**: System fonts for optimal readability
- **Layout**: Flexbox-based responsive design with centered max-width
- **Animations**: Smooth transitions, hover effects, and loading states
- **Accessibility**: ARIA labels and keyboard navigation
- **Icons**: Custom SVG icons for all actions

## 🔌 API Endpoints

### Streaming Chat (Primary)
```http
POST /api/chat/stream
Content-Type: application/json

{
  "message": "User message",
  "conversation_history": [],  // Optional
  "session_id": "string"       // Optional
}

Response: Server-Sent Events
data: {"type": "step", "content": "simple"}  // Routing decision
data: {"type": "token", "content": "AI"}
data: {"type": "token", "content": " supports"}
data: {"type": "sources", "content": [...]} // Source documents
```

### Health Check
```http
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-10-01T12:00:00",
  "features": {
    "streaming": true,
    "langsmith": true
  }
}
```

### Interactive API Documentation
Visit http://localhost:8000/docs for full interactive Swagger documentation.

## ⚙️ Configuration

### API Environment Variables (api/.env)

```bash
# Required
OPENAI_API_KEY=sk-...          # Your OpenAI API key
OPENAI_MODEL=gpt-4             # Model for agent responses
PINECONE_API_KEY=...           # Pinecone vector store API key
PINECONE_ENVIRONMENT=...       # e.g., us-east-1-aws
PINECONE_INDEX_NAME=...        # Your index name

# Optional
TAVILY_API_KEY=...             # For web search (optional)
LANGCHAIN_API_KEY=...          # For LangSmith tracing (optional)
LANGCHAIN_TRACING_V2=true      # Enable tracing
```

### Ingest Environment Variables (ingest/.env)

```bash
# Required
OPENAI_API_KEY=sk-...          # For embeddings
PINECONE_API_KEY=...           # Vector store
PINECONE_ENVIRONMENT=...       
PINECONE_INDEX_NAME=...        
```

### Frontend Configuration

The UI automatically connects to the API at `http://localhost:8000` during development.

## 🐳 Docker

### Development Mode
```bash
docker-compose -f docker-compose.dev.yml up
```
- **Frontend**: React dev server with hot reload on port 3000
- **API**: FastAPI with uvicorn auto-reload on port 8000
- Volume mounts for live code updates

### Production Mode
```bash
docker-compose up --build
```
- **Frontend**: Nginx serving optimized React build
- **API**: FastAPI with production settings
- Multi-stage builds for smaller images

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🛠️ Makefile Commands

The project includes a comprehensive Makefile for easy development:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make start` | Start all services (auto-detects Docker availability) |
| `make stop` | Stop all running services |
| `make ui` | Start only the UI development server |
| `make api` | Start only the API server (when implemented) |
| `make build` | Build all services for production |
| `make install` | Install dependencies for all services |
| `make test` | Run all tests |
| `make test-ui` | Run UI tests only |
| `make check` | Check TypeScript compilation |
| `make status` | Show status of running services |
| `make logs` | Show logs from running services |
| `make clean` | Clean build artifacts and dependencies |

## 🎯 Example Use Cases

### Simple Queries (Automatic RAG)
- **Definitions**: "What is machine learning?"
- **Explanations**: "How does neural network training work?"
- **Comparisons**: "Compare SQL and NoSQL databases"
- **History**: "History of computing"
- **How-to**: "How does AI support exploring Mars?"

### Research Queries (Multi-Agent)
- **Reports**: "Write a comprehensive report on renewable energy"
- **Analysis**: "Research and write about quantum computing applications"
- **Deep Dives**: "Create a detailed report on blockchain technology"

## 🔮 Future Enhancements

### Potential Features
- ✨ **Multi-modal Support**: Image and document upload
- ✨ **Conversation Memory**: Persistent conversation threads with database
- ✨ **User Authentication**: Multi-user support with auth
- ✨ **Custom Knowledge Bases**: Per-user or per-organization document collections
- ✨ **Advanced Citations**: Click-through to source documents with highlighting
- ✨ **Voice Interface**: Speech-to-text and text-to-speech
- ✨ **Collaborative Features**: Share conversations and reports
- ✨ **API Rate Limiting**: User-based quotas and rate limits
- ✨ **Analytics Dashboard**: Usage metrics and popular queries

### Infrastructure
- 🚀 **CI/CD Pipeline**: Automated testing and deployment
- 🚀 **Production Deployment**: Kubernetes or cloud deployment
- 🚀 **Monitoring**: Application performance monitoring
- 🚀 **Caching**: Redis for response caching

## 🤝 Contributing

1. Follow existing code patterns and TypeScript conventions
2. Write tests for new functionality
3. Ensure all tests pass before submitting
4. Use meaningful commit messages

## 📄 License

This project is a demonstration application for AI chat interfaces.