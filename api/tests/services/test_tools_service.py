"""
Tests for agent tools.
Testing RAG tools, web search tools, and research tools.
"""

from unittest.mock import patch

import pytest

from ..factories import VectorStoreFactory


class TestKnowledgeBaseSearchTool:
    """Tests for knowledge base search tool."""

    @pytest.mark.asyncio
    async def test_search_knowledge_base(self):
        """Test knowledge base search tool."""
        from tools import search_knowledge_base

        # Use factory directly - no fixture needed
        mock_vector_store = VectorStoreFactory.create_mock_vector_store()

        with patch("tools.vector_store_service", mock_vector_store):
            result = await search_knowledge_base.ainvoke({"query": "What is RAG?"})

            assert "RAG systems combine retrieval" in result
            assert "[KB-1]" in result
            assert "KNOWLEDGE BASE SOURCES" in result
            mock_vector_store.similarity_search_with_score.assert_called_once()

    @pytest.mark.asyncio
    async def test_search_knowledge_base_no_results(self):
        """Test knowledge base search with no results."""
        from tools import search_knowledge_base

        # Use factory directly - no fixture needed
        empty_vector_store = VectorStoreFactory.create_empty_vector_store()

        with patch("tools.vector_store_service", empty_vector_store):
            result = await search_knowledge_base.ainvoke({"query": "Unknown topic"})

            assert "No relevant information found" in result


class TestResearchTools:
    """Tests for research-related tools."""

    @pytest.mark.asyncio
    async def test_research_topic_breakdown(self):
        """Test research topic breakdown tool."""
        from tools import research_topic_breakdown

        result = await research_topic_breakdown.ainvoke({"topic": "Vector Databases"})

        assert "Vector Databases" in result
        assert "Research Topic Breakdown" in result
        assert "Suggested Research Approach" in result
        assert "Key Research Questions" in result

    @pytest.mark.asyncio
    async def test_create_report_outline(self):
        """Test report outline creation tool."""
        from tools import create_report_outline

        result = await create_report_outline.ainvoke(
            {
                "topic": "AI in Healthcare",
                "findings_summary": "Key findings about AI applications",
            }
        )

        assert "AI in Healthcare" in result
        assert "## Executive Summary" in result
        assert "## References" in result
        assert "KB-X" in result  # Citation format
        assert "WEB-X" in result  # Web citation format


class TestWebSearchTool:
    """Tests for web search tool creation."""

    def test_create_web_search_tool_with_api_key(self, mock_env_vars):
        """Test creating web search tool with API key."""
        from tools import create_web_search_tool

        with patch("tools.settings.tavily_api_key", "test-tavily-key"):
            tool = create_web_search_tool()

            assert tool is not None

    def test_create_web_search_tool_without_api_key(self):
        """Test creating web search tool without API key."""
        from tools import create_web_search_tool

        with patch("tools.settings.tavily_api_key", None):
            tool = create_web_search_tool()

            assert tool is None


class TestToolCollection:
    """Tests for tool collection and availability."""

    def test_get_available_tools(self, mock_env_vars):
        """Test getting list of available tools."""
        from tools import get_available_tools

        with patch("tools.settings.tavily_api_key", "test-key"):
            tools = get_available_tools()

            assert len(tools) >= 3  # At least the basic tools

            # Check tool names
            tool_names = [t.name for t in tools]
            assert "research_topic_breakdown" in tool_names
            assert "search_knowledge_base" in tool_names
            assert "create_report_outline" in tool_names

    def test_get_available_tools_with_web_search(self, mock_env_vars):
        """Test that web search is included when API key is available."""
        from tools import get_available_tools

        with patch("tools.settings.tavily_api_key", "test-key"):
            tools = get_available_tools()

            # Should include web search with tavily_api_key
            assert len(tools) >= 4

    def test_get_available_tools_without_web_search(self):
        """Test that web search is excluded when no API key."""
        from tools import get_available_tools

        with patch("tools.settings.tavily_api_key", None):
            tools = get_available_tools()

            # Should not include web search
            tool_names = [t.name for t in tools]
            assert "tavily_search_results_json" not in tool_names
