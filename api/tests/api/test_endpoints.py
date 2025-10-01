"""
Tests for FastAPI endpoints.
Unit tests only - integration tests marked for future implementation.
"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from models import ChatRequest

from ..factories import AgentFactory


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    @pytest.fixture
    def client(self, mock_env_vars):
        """Create test client."""
        # Mock agent creation to avoid real API initialization
        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            return TestClient(app)

    def test_root_endpoint(self, client):
        """Test root health check endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "features" in data

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_features_endpoint_includes_capabilities(self, client):
        """Test that features endpoint shows all capabilities."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "web_search" in data["features"]
        assert "rag" in data["features"]
        assert "langsmith" in data["features"]


class TestChatEndpointValidation:
    """Tests for chat endpoint request validation."""

    @pytest.fixture
    def client(self, mock_env_vars):
        """Create test client."""
        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            return TestClient(app)

    def test_chat_endpoint_validation_error(self, client):
        """Test chat endpoint with invalid request."""
        invalid_request = {"message": ""}  # Empty message

        response = client.post("/api/chat", json=invalid_request)

        assert response.status_code == 422  # Validation error


class TestCORSConfiguration:
    """Tests for CORS configuration."""

    @pytest.fixture
    def client(self, mock_env_vars):
        """Create test client."""
        with patch("agent.ChatOpenAI"), patch("agent.get_available_tools", return_value=[]):
            from main import app

            return TestClient(app)

    def test_cors_headers(self, client):
        """Test CORS headers are set."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers


class TestStreamingFunctionality:
    """Tests for streaming chat functionality (unit tests)."""

    @pytest.mark.asyncio
    async def test_generate_chat_stream(self, sample_chat_request_dict):
        """Test chat stream generation with mocked agent."""
        from main import generate_chat_stream

        # Use factory directly
        mock_agent = AgentFactory.create_mock_agent()
        request = ChatRequest(**sample_chat_request_dict)

        with patch("main.agent", mock_agent):
            chunks = []
            async for chunk in generate_chat_stream(request):
                chunks.append(chunk)

            assert len(chunks) > 0
            # Chunks are JSON strings (EventSourceResponse adds "data: " prefix later)
            assert all(isinstance(chunk, str) for chunk in chunks)
            # Verify we got expected chunk types
            import json

            chunk_data = [json.loads(chunk) for chunk in chunks]
            assert any(c["type"] == "token" for c in chunk_data)
            assert any(c["type"] == "done" for c in chunk_data)

    @pytest.mark.asyncio
    async def test_generate_chat_stream_handles_errors(self, sample_chat_request_dict):
        """Test chat stream handles errors gracefully."""
        from main import generate_chat_stream

        # Use factory to create error agent
        mock_agent = AgentFactory.create_mock_agent_with_error()

        request = ChatRequest(**sample_chat_request_dict)

        with patch("main.agent", mock_agent):
            chunks = []
            async for chunk in generate_chat_stream(request):
                chunks.append(chunk)

            # Should have error chunk
            assert len(chunks) > 0
            error_chunk_found = any("error" in chunk for chunk in chunks)
            assert error_chunk_found
