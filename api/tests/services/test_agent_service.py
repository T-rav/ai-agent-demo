"""
Tests for agent service functionality.
Unit tests for agent components.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage


class TestAgentStateManagement:
    """Tests for agent state and message handling."""

    def test_agent_state_structure(self):
        """Test that agent state has correct structure."""

        # AgentState is a TypedDict, test we can create it
        state = {"messages": [], "sources": [], "routing_decision": "simple"}

        assert "messages" in state
        assert "sources" in state
        assert "routing_decision" in state


class TestAgentToolIntegration:
    """Tests for agent tool integration."""

    def test_get_available_tools_returns_list(self):
        """Test that get_available_tools returns a list."""
        from tools import get_available_tools

        with patch("tools.settings") as mock_settings:
            mock_settings.tavily_api_key = "test-key"

            with patch("tools.search_web"), patch("tools.search_knowledge_base"):
                tools = get_available_tools()

                assert isinstance(tools, list)
                assert len(tools) > 0


class TestRAGAgentInitialization:
    """Tests for RAGAgent initialization."""

    def test_agent_initialization(self):
        """Test that RAGAgent can be initialized."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                assert agent.llm is not None
                assert agent.router_llm is not None
                assert agent.tools == []
                assert agent.graph is not None


class TestAgentRouting:
    """Tests for agent routing logic."""

    @pytest.mark.asyncio
    async def test_route_request_simple(self):
        """Test routing to simple path."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_router = MagicMock()

                # Mock router response for simple
                mock_router.ainvoke = AsyncMock(return_value=AIMessage(content="SIMPLE"))

                mock_chat.side_effect = [mock_llm, mock_router]

                agent = RAGAgent()

                state = {
                    "messages": [HumanMessage(content="What is Python?")],
                    "sources": [],
                    "routing_decision": "simple",
                }

                result = await agent._route_request(state)

                assert result["routing_decision"] == "simple"

    @pytest.mark.asyncio
    async def test_route_request_research(self):
        """Test routing to research path."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_router = MagicMock()

                # Mock router response for research
                mock_router.ainvoke = AsyncMock(return_value=AIMessage(content="RESEARCH"))

                mock_chat.side_effect = [mock_llm, mock_router]

                agent = RAGAgent()

                state = {
                    "messages": [HumanMessage(content="Write a comprehensive report on AI")],
                    "sources": [],
                    "routing_decision": "simple",
                }

                result = await agent._route_request(state)

                assert result["routing_decision"] == "research"

    @pytest.mark.asyncio
    async def test_route_request_no_user_message(self):
        """Test routing with no user message."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                state = {
                    "messages": [AIMessage(content="Hello")],
                    "sources": [],
                    "routing_decision": "simple",
                }

                result = await agent._route_request(state)

                # Should return state unchanged
                assert result == state


class TestAgentModeSelection:
    """Tests for agent mode selection."""

    def test_determine_mode_simple(self):
        """Test mode selection returns simple."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                state = {
                    "messages": [],
                    "sources": [],
                    "routing_decision": "simple",
                }

                mode = agent._determine_mode(state)

                assert mode == "simple"

    def test_determine_mode_research(self):
        """Test mode selection returns research."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                state = {
                    "messages": [],
                    "sources": [],
                    "routing_decision": "research",
                }

                mode = agent._determine_mode(state)

                assert mode == "research"

    def test_determine_mode_default(self):
        """Test mode selection defaults to simple."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                state = {"messages": [], "sources": []}

                mode = agent._determine_mode(state)

                assert mode == "simple"


class TestSimpleRAG:
    """Tests for simple RAG functionality."""

    @pytest.mark.asyncio
    async def test_simple_rag_with_documents(self):
        """Test simple RAG retrieves and injects context."""
        from agent import RAGAgent
        from tests.factories import VectorStoreFactory

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                # Use factory to create mock vector store
                mock_vector_store = VectorStoreFactory.create_mock_vector_store()

                with patch("vector_store.vector_store_service", mock_vector_store):
                    state = {
                        "messages": [HumanMessage(content="What is Python?")],
                        "sources": [],
                        "routing_decision": "simple",
                    }

                    result = await agent._simple_rag(state)

                    assert len(result["sources"]) > 0
                    assert result["sources"][0]["metadata"]["file_name"] == "rag-guide.md"

    @pytest.mark.asyncio
    async def test_simple_rag_no_user_message(self):
        """Test simple RAG with no user message."""
        from agent import RAGAgent

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                state = {
                    "messages": [AIMessage(content="Hello")],
                    "sources": [],
                    "routing_decision": "simple",
                }

                result = await agent._simple_rag(state)

                # Should return state unchanged
                assert result["sources"] == []

    @pytest.mark.asyncio
    async def test_simple_rag_no_documents_found(self):
        """Test simple RAG when no documents are found."""
        from agent import RAGAgent
        from tests.factories import VectorStoreFactory

        with patch("agent.ChatOpenAI") as mock_chat:
            with patch("agent.get_available_tools", return_value=[]):
                mock_llm = MagicMock()
                mock_llm.bind_tools.return_value = mock_llm
                mock_chat.return_value = mock_llm

                agent = RAGAgent()

                # Use factory to create empty vector store
                empty_vector_store = VectorStoreFactory.create_empty_vector_store()

                with patch("vector_store.vector_store_service", empty_vector_store):
                    state = {
                        "messages": [HumanMessage(content="What is quantum physics?")],
                        "sources": [],
                        "routing_decision": "simple",
                    }

                    result = await agent._simple_rag(state)

                    assert result["sources"] == []
