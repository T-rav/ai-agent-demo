"""
Tools for the LangGraph research agent.
"""

from typing import Dict, List, Optional

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from config import settings
from vector_store import vector_store_service


@tool
async def search_knowledge_base(query: str) -> str:
    """
    Search the AI and Computing knowledge base for in-depth information.
    Use this for foundational concepts, established theories, and technical background.

    Best for: AI concepts, computing history, machine learning fundamentals, algorithms.

    IMPORTANT: Track the sources returned! Use the [KB-X] identifiers to cite them in your report.

    Args:
        query: Specific research question or topic

    Returns:
        Relevant information with metadata from knowledge base
    """
    # Retrieve relevant documents
    docs_with_scores = await vector_store_service.similarity_search_with_score(query, k=5)

    if not docs_with_scores:
        return "No relevant information found in the knowledge base."

    # Format results with source citations for tracking
    results = []
    sources_section = "\n\n=== KNOWLEDGE BASE SOURCES (Cite these in your References) ===\n"

    for i, (doc, score) in enumerate(docs_with_scores, 1):
        content = doc.page_content
        metadata = doc.metadata

        # Extract source information (match ingestion field names)
        source_file = metadata.get("file_name", metadata.get("source", "Unknown"))
        doc_title = metadata.get("document_title", metadata.get("title", "Untitled"))
        section_header = metadata.get("section_header")

        # Use document title, but add section context if available
        if section_header:
            display_title = f"{source_file}: {section_header}"
        else:
            display_title = doc_title if doc_title != "Untitled" else source_file

        # Content with citation identifier
        results.append(
            f"[KB-{i}] {display_title}\n"
            f"From: {source_file}\n"
            f"Relevance: {score:.3f}\n\n"
            f"{content}\n"
        )

        # Track source for references (use clean file name without extension)
        clean_source = source_file.replace('.md', '').replace('_', ' ').title()
        sources_section += f"[KB-{i}] {clean_source} ({source_file})\n"

    return "\n---\n\n".join(results) + sources_section


@tool
async def research_topic_breakdown(topic: str) -> str:
    """
    Break down a research topic into key subtopics and research questions.
    Use this FIRST to plan your research approach for comprehensive coverage.

    Args:
        topic: The main research topic

    Returns:
        Structured breakdown of subtopics and research questions
    """
    # This is a meta-tool that guides the research process
    # In a real implementation, this could use an LLM to generate the breakdown
    # For now, we'll provide a structured template

    breakdown = f"""
Research Topic Breakdown: {topic}

Suggested Research Approach:
1. Define core concepts and terminology
2. Explore historical context and evolution
3. Analyze current state and technologies
4. Identify key challenges and limitations
5. Examine future trends and predictions
6. Review real-world applications and case studies

Key Research Questions:
- What are the fundamental concepts underlying {topic}?
- How has {topic} evolved over time?
- What are the current state-of-the-art approaches?
- What are the major challenges or controversies?
- What are the practical applications and use cases?
- What does the future hold for {topic}?

Recommended Sources:
- Knowledge Base: For foundational concepts and established theories
- Web Search: For latest developments, recent research, and current trends
"""

    return breakdown


@tool
async def synthesize_research_findings(findings: List[str]) -> str:
    """
    Synthesize multiple research findings into coherent insights.
    Use this after gathering information from multiple sources.

    Args:
        findings: List of research findings or information chunks

    Returns:
        Synthesized insights identifying patterns, contradictions, and key themes
    """
    # This is a meta-tool that helps organize research
    synthesis = f"""
Synthesis Guidelines:

1. Identify Common Themes:
   - What concepts appear across multiple sources?
   - What are the consensus views?

2. Note Contradictions or Debates:
   - Where do sources disagree?
   - What are different perspectives?

3. Highlight Key Insights:
   - What are the most important findings?
   - What stands out as significant?

4. Identify Gaps:
   - What questions remain unanswered?
   - What areas need more research?

Total findings to synthesize: {len(findings)}
"""

    return synthesis


@tool
async def create_report_outline(topic: str, findings_summary: str) -> str:
    """
    Create a structured MARKDOWN outline for a research report.
    Use this after gathering research to organize your final report.

    Args:
        topic: The research topic
        findings_summary: Summary of key findings

    Returns:
        Structured MARKDOWN report outline with sections
    """
    outline = f"""
Research Report Outline: {topic}

## Executive Summary
Brief overview of topic and key findings (cite sources: KB-X, WEB-X)

## Introduction
- Topic definition and scope
- Importance and relevance
- Research methodology

## Background and Context
- Historical development (cite KB sources)
- Foundational concepts (cite KB sources)
- Key terminology

## Current State of the Field
- State-of-the-art approaches (cite WEB sources for recent)
- Major technologies and techniques
- Leading research and practitioners

## Analysis and Findings
- Key insights from research (cite all sources)
- Comparison of different approaches
- Case studies and applications (cite WEB sources)

## Challenges and Limitations
- Current obstacles
- Controversies or debates
- Areas of uncertainty

## Future Directions
- Emerging trends (cite WEB sources)
- Predictions and possibilities
- Open research questions

## Conclusion
- Summary of key takeaways
- Implications and recommendations

## References

### Knowledge Base Sources
[KB-1] Title (source file)
[KB-2] Title (source file)
...

### Web Sources
[WEB-1] Title (URL)
[WEB-2] Title (URL)
...

IMPORTANT: Make sure to populate the References section with ALL sources you used!
"""

    return outline


class WebSearchTool:
    """Stateful web search tool that maintains global source numbering."""

    def __init__(self):
        self.source_counter = 0

    async def search(self, query: str) -> str:
        """
        Search the web for latest information, recent research, and current trends.
        Use this for recent developments, current events, and real-world examples.

        IMPORTANT: Track the sources returned! Use the [WEB-X] identifiers to cite them in your report.

        Args:
            query: Specific search query

        Returns:
            Relevant web search results with URLs for citations
        """
        if not settings.tavily_api_key:
            return "Web search is not available (no API key configured)."

        try:
            from langchain_community.tools.tavily_search import TavilySearchResults

            search_tool = TavilySearchResults(
                api_key=settings.tavily_api_key,
                max_results=5,
                search_depth="advanced",
                include_domains=["arxiv.org", "github.com", "medium.com", "towardsdatascience.com"],
            )

            # Execute search
            results = await search_tool.ainvoke(query)

            if not results:
                return "No web results found for this query."

            # Format results with clear source tracking using global counter
            formatted_results = []
            sources_section = "\n\n=== WEB SOURCES (Cite these in your References) ===\n"

            for result in results:
                self.source_counter += 1
                source_num = self.source_counter

                title = result.get("title", "Untitled")
                url = result.get("url", "Unknown URL")
                content = result.get("content", "")

                formatted_results.append(
                    f"[WEB-{source_num}] {title}\n"
                    f"URL: {url}\n\n"
                    f"{content}\n"
                )

                sources_section += f"[WEB-{source_num}] {title} ({url})\n"

            return "\n---\n\n".join(formatted_results) + sources_section

        except Exception as e:
            return f"Error performing web search: {str(e)}"

    def as_tool(self):
        """Convert to LangChain tool."""
        return tool(self.search)


def create_web_search_tool() -> Optional[WebSearchTool]:
    """
    Create a stateful web search tool for finding latest information and research.

    Returns:
        WebSearchTool instance that maintains global source numbering
    """
    if not settings.tavily_api_key:
        return None

    return WebSearchTool()


# List of available tools
def get_available_tools():
    """Get list of available tools for the research agent.

    Note: Web search tool is NOT included here as it's created per-request
    to maintain isolated source counters for concurrent requests.
    """
    tools = [
        research_topic_breakdown,
        search_knowledge_base,
        create_report_outline,
    ]

    return tools
