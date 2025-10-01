"""
AI Agent API with RAG capabilities using LangChain, LangGraph, and LangSmith.
"""

import os
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from agent import agent
from config import settings
from models import ChatRequest, ChatResponse, SourceDocument, StreamChunk

# Set up LangSmith tracing
if settings.langchain_tracing_v2 and settings.langchain_api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project

app = FastAPI(
    title="AI Agent API",
    version="0.1.0",
    description="RAG system with LangChain, LangGraph, and web search capabilities",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "AI Agent API is running",
        "version": "0.1.0",
        "features": {
            "rag": True,
            "web_search": settings.tavily_api_key is not None,
            "langsmith": settings.langchain_tracing_v2 and settings.langchain_api_key is not None,
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


async def generate_chat_stream(request: ChatRequest) -> AsyncIterator[str]:
    """
    Generate streaming response from the agent.

    Args:
        request: Chat request with message and history

    Yields:
        Server-sent events with response chunks
    """
    try:
        # Build messages list from conversation history
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.conversation_history
        ]

        # Add the current message
        messages.append({"role": "user", "content": request.message})

        # Stream the response
        async for chunk in agent.astream(messages, session_id=request.session_id):
            # Convert chunk to StreamChunk model
            stream_chunk = StreamChunk(**chunk)

            # Yield JSON (EventSourceResponse will add "data: " prefix)
            yield stream_chunk.model_dump_json()

    except Exception as e:
        # Send error chunk
        error_chunk = StreamChunk(type="error", error=str(e))
        yield error_chunk.model_dump_json()


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint with RAG and web search.

    This endpoint uses LangGraph to orchestrate:
    1. Knowledge base retrieval (RAG)
    2. Web search (when needed)
    3. LLM generation with streaming

    LangSmith tracing is enabled for observability.

    Args:
        request: Chat request with message and optional conversation history

    Returns:
        Server-sent events stream with response chunks
    """
    return EventSourceResponse(generate_chat_stream(request))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Non-streaming chat endpoint.

    Args:
        request: Chat request

    Returns:
        Complete chat response with sources
    """
    try:
        # Build messages list
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.conversation_history
        ]
        messages.append({"role": "user", "content": request.message})

        # Get response from agent
        result = await agent.ainvoke(messages, session_id=request.session_id)

        # Convert sources to SourceDocument models
        sources = [SourceDocument(**source) for source in result.get("sources", [])]

        return ChatResponse(
            message=result["message"], sources=sources, session_id=request.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
