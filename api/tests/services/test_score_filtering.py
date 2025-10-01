"""
Tests for score threshold filtering in RAG.
"""

from unittest.mock import AsyncMock, patch

import pytest


class TestScoreThresholdFiltering:
    """Tests for score threshold filtering in knowledge base search."""

    @pytest.mark.asyncio
    async def test_filters_low_score_documents(self, mock_env_vars):
        """Test that documents below threshold are filtered out."""
        from langchain_core.documents import Document

        from tools import search_knowledge_base

        # Create documents with varying scores
        high_score_doc = Document(
            page_content="Relevant content",
            metadata={"file_name": "good.md", "document_title": "Good Document"},
        )
        low_score_doc = Document(
            page_content="Less relevant content",
            metadata={"file_name": "bad.md", "document_title": "Bad Document"},
        )

        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(
            return_value=[
                (high_score_doc, 0.75),
                (low_score_doc, 0.3),
            ]  # 0.3 is below 0.5 threshold
        )

        with patch("tools.vector_store_service", mock_vs):
            result = await search_knowledge_base.ainvoke({"query": "test"})

            # Should only include high score document
            assert "Good Document" in result
            assert "Bad Document" not in result
            assert "[KB-1]" in result
            assert "[KB-2]" not in result  # Should only have 1 source

    @pytest.mark.asyncio
    async def test_returns_message_when_all_below_threshold(self, mock_env_vars):
        """Test that helpful message is returned when all docs below threshold."""
        from langchain_core.documents import Document

        from tools import search_knowledge_base

        low_score_doc = Document(
            page_content="Low relevance content",
            metadata={"file_name": "low.md", "document_title": "Low Score Doc"},
        )

        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(
            return_value=[(low_score_doc, 0.2), (low_score_doc, 0.3)]  # All below 0.5
        )

        with patch("tools.vector_store_service", mock_vs):
            result = await search_knowledge_base.ainvoke({"query": "test"})

            assert "No relevant information found above the similarity threshold" in result
            assert "Low Score Doc" not in result

    @pytest.mark.asyncio
    async def test_passes_documents_at_threshold(self, mock_env_vars):
        """Test that documents exactly at threshold pass through."""
        from langchain_core.documents import Document

        from tools import search_knowledge_base

        threshold_doc = Document(
            page_content="At threshold",
            metadata={"file_name": "threshold.md", "document_title": "Threshold Doc"},
        )

        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(
            return_value=[(threshold_doc, 0.5)]  # Exactly at threshold
        )

        with patch("tools.vector_store_service", mock_vs):
            result = await search_knowledge_base.ainvoke({"query": "test"})

            assert "Threshold Doc" in result
            assert "[KB-1]" in result


class TestSimpleRAGScoreFiltering:
    """Tests for score filtering in simple RAG flow."""

    @pytest.mark.asyncio
    async def test_simple_rag_filters_low_scores(self, mock_env_vars):
        """Test that _simple_rag filters documents below threshold."""
        from langchain_core.documents import Document
        from langchain_core.messages import HumanMessage

        from agent import RAGAgent

        # Create mock documents
        high_score_doc = Document(
            page_content="Relevant answer",
            metadata={"file_name": "good.md", "document_title": "Good Source", "chunk_index": 0},
        )
        low_score_doc = Document(
            page_content="Irrelevant answer",
            metadata={"file_name": "bad.md", "document_title": "Bad Source", "chunk_index": 0},
        )

        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(
            return_value=[(high_score_doc, 0.8), (low_score_doc, 0.2)]
        )

        with patch("vector_store.vector_store_service", mock_vs):
            agent = RAGAgent()
            state = {"messages": [HumanMessage(content="test query")], "sources": []}

            result = await agent._simple_rag(state)

            # Should only include high score source
            assert len(result["sources"]) == 1
            assert result["sources"][0]["metadata"]["document_title"] == "Good Source"

    @pytest.mark.asyncio
    async def test_simple_rag_handles_no_sources_above_threshold(self, mock_env_vars):
        """Test that _simple_rag handles case when no sources pass threshold."""
        from langchain_core.documents import Document
        from langchain_core.messages import HumanMessage, SystemMessage

        from agent import RAGAgent

        low_score_doc = Document(
            page_content="Low relevance",
            metadata={"file_name": "low.md", "document_title": "Low Doc", "chunk_index": 0},
        )

        mock_vs = AsyncMock()
        mock_vs.similarity_search_with_score = AsyncMock(
            return_value=[(low_score_doc, 0.3), (low_score_doc, 0.2)]
        )

        with patch("vector_store.vector_store_service", mock_vs):
            agent = RAGAgent()
            state = {"messages": [HumanMessage(content="test query")], "sources": []}

            result = await agent._simple_rag(state)

            # Should have no sources
            assert len(result.get("sources", [])) == 0

            # Should have a system message about no relevant information
            messages = result["messages"]
            system_messages = [m for m in messages if isinstance(m, SystemMessage)]
            assert len(system_messages) > 0
            assert "No relevant information found" in system_messages[0].content
