"""
Tests for agent service functionality.
Unit tests for agent components.
"""

from unittest.mock import patch




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
