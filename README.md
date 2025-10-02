# 🤖 AI Assistant Demo

![AI Assistant Demo](./docs/screenshot.png)

> Production-ready AI assistant with intelligent routing, RAG with source citations, and a beautiful React TypeScript frontend.

## 🚀 Features

- **Intelligent Routing** - GPT-4o-mini classifies queries as simple or research
- **RAG with Citations** - Automatic Pinecone vector search with source documents
- **Multi-Agent Research** - Planner → Gatherer → Report Builder workflow
- **Real-time Streaming** - Token-by-token responses via Server-Sent Events
- **Export to Markdown** - Download conversations with sources and metadata
- **Beautiful UI** - Dark theme with mode indicators and expandable sources

**Tech Stack:** React, TypeScript, FastAPI, LangGraph, OpenAI GPT-4, Pinecone, Tavily

## ⚡ Quick Start

```bash
# 1. Setup environment variables
cp api/env.example api/.env
cp ingest/env.example ingest/.env
# Edit both .env files with your API keys (OpenAI, Pinecone, Tavily optional)

# 2. Ingest knowledge base (one-time setup)
cd ingest && make dev-install && make run

# 3. Start the application
cd .. && make start
```

**Access:**
- UI: http://localhost:3000
- API: http://localhost:8000

## 📖 Usage

**Simple queries** (automatic RAG):
- "What is deep learning?"
- "How does AI support exploring Mars?"

**Research mode** (multi-agent):
- "Write a comprehensive report on AI in healthcare"
- "Research quantum computing and create a detailed report"

## 📐 Architecture

Want to understand how it works? Check out the [detailed architecture documentation](./docs/ARCHITECTURE.md) for:
- System design and workflow diagrams
- Multi-agent orchestration with LangGraph
- Intelligent routing decisions
- RAG implementation details
- Citation system

## 🧪 Testing

```bash
cd ui && npm test        # Frontend tests
cd api && pytest         # Backend tests
cd ingest && pytest      # Ingest tests
```
