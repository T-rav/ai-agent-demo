"""
LangGraph agent for RAG with web search capabilities.
"""

from typing import Annotated, List, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import settings
from tools import get_available_tools


# Define the agent state
class AgentState(TypedDict):
    """State for the agent graph."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    sources: List[dict]
    routing_decision: str  # "simple" or "research"
    web_source_counter: int  # Global counter for web sources across searches


class RAGAgent:
    """RAG agent using LangGraph for workflow orchestration."""

    def __init__(self):
        """Initialize the RAG agent."""
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            temperature=0.7,
            streaming=True,
        )

        # Separate LLM for routing decisions (faster, cheaper)
        self.router_llm = ChatOpenAI(
            model="gpt-3.5-turbo",  # Faster for routing
            openai_api_key=settings.openai_api_key,
            temperature=0,
        )

        self.tools = get_available_tools()
        self.llm_with_tools = self.llm.bind_tools(self.tools)

        # Build the graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow with intelligent routing."""
        workflow = StateGraph(AgentState)

        # Define nodes
        workflow.add_node("router", self._route_request)  # 1. Classifies request

        # Simple path nodes
        workflow.add_node("simple_rag", self._simple_rag)  # Simple: Auto RAG
        workflow.add_node("simple_agent", self._simple_agent)  # Simple: Answer

        # Research path nodes (multi-step workflow)
        workflow.add_node("research_planner", self._research_planner)  # Research: Plan topics
        workflow.add_node("research_gatherer", self._research_gatherer)  # Research: Gather info
        workflow.add_node("report_builder", self._report_builder)  # Research: Build report

        # Tool execution (shared)
        workflow.add_node("tools", ToolNode(self.tools))

        # Define edges with routing
        workflow.set_entry_point("router")  # Start with router

        # Router decides path
        workflow.add_conditional_edges(
            "router",
            self._determine_mode,
            {
                "research": "research_planner",  # Research → planning phase
                "simple": "simple_rag",  # Simple → auto RAG
            },
        )

        # === SIMPLE PATH ===
        # simple_rag → simple_agent → END (or web tool if needed)
        workflow.add_edge("simple_rag", "simple_agent")
        workflow.add_conditional_edges(
            "simple_agent", self._should_continue, {"continue": "tools", "end": END}
        )

        # === RESEARCH PATH ===
        # Step 1: Planner → tools → gatherer
        workflow.add_edge("research_planner", "tools")  # Execute planning tools
        workflow.add_edge("tools", "research_gatherer")  # Then gather info

        # Step 2: Gatherer decides if needs more tools or ready to build
        workflow.add_conditional_edges(
            "research_gatherer",
            self._check_research_ready,
            {
                "gather_more": "tools",  # Need more info → back to tools
                "build_report": "report_builder",  # Have enough → build report
            },
        )

        # Step 3: Report builder → END
        workflow.add_edge("report_builder", END)

        return workflow.compile()

    async def _route_request(self, state: AgentState) -> AgentState:
        """
        Intelligently route the request to determine if it needs deep research or simple answer.
        This is the first node - it analyzes user intent.

        Args:
            state: Current agent state

        Returns:
            Updated state with routing decision
        """
        messages = state["messages"]

        # Get the user's latest message
        user_message = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                user_message = msg.content
                break

        if not user_message:
            return state

        # Ask the router LLM to classify the request
        routing_prompt = f"""Analyze this user request and determine if it requires:
A) SIMPLE answer (quick fact, definition, brief explanation)
B) RESEARCH (comprehensive report, deep analysis, detailed exploration)

User request: "{user_message}"

IMPORTANT: Definitional questions are ALWAYS simple, regardless of topic complexity.

Simple indicators (ALWAYS route to SIMPLE):
- Direct definitional questions: "What is...", "What are...", "Define...", "Explain what..."
- Questions about who/when/where: "Who invented...", "When did...", "Where was..."
- Questions about history/background: "history of...", "background of...", "evolution of..."
- Requests for definitions, concepts, or brief explanations
- Quick facts or single-source answers
- Examples: "What is RAG?", "What is deep learning?", "history of computing", "evolution of AI"

Research indicators (ONLY these trigger RESEARCH):
- Explicit research keywords: "comprehensive", "research", "write a report", "deep dive into", "in-depth analysis"
- Multi-part analysis requests: "analyze and compare", "trace the development of", "conduct research on"
- Requests for structured multi-section content: "write a detailed report", "create a comprehensive guide"
- Requests that explicitly need multiple sources or perspectives
- Complex analytical questions requiring synthesis across multiple topics

Respond with ONLY ONE WORD:
- "RESEARCH" if this needs comprehensive research
- "SIMPLE" if this needs a quick answer"""

        routing_response = await self.router_llm.ainvoke([HumanMessage(content=routing_prompt)])

        # Store routing decision in state metadata
        decision = "research" if "RESEARCH" in routing_response.content.upper() else "simple"

        # Add routing decision as metadata to state
        if "routing_decision" not in state:
            state["routing_decision"] = decision

        return state

    def _determine_mode(self, state: AgentState) -> str:
        """
        Determine which path to take based on routing decision.

        Args:
            state: Current agent state

        Returns:
            Path string: "research" or "simple"
        """
        decision = state.get("routing_decision", "simple")
        return decision

    async def _simple_rag(self, state: AgentState) -> AgentState:
        """
        Handle simple RAG path - automatically retrieve and inject context.
        This is a separate node for the simple path.

        Args:
            state: Current agent state

        Returns:
            Updated state with RAG context injected
        """
        messages = state["messages"]

        # Get the user's query
        user_query = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                user_query = msg.content
                break

        if user_query:
            # Automatic RAG retrieval
            from vector_store import vector_store_service

            docs_with_scores = await vector_store_service.similarity_search_with_score(
                user_query, k=3
            )

            # Build context from retrieved documents and track sources
            if docs_with_scores:
                context_parts = []
                sources_list = []
                seen_sources = set()  # Track unique (file_name, title) pairs

                source_number = 1
                for doc, score in docs_with_scores:
                    # Extract metadata (use correct field names from ingestion)
                    source_file = doc.metadata.get("file_name", "Unknown")
                    title = doc.metadata.get("document_title", "Untitled")

                    # Create unique key for deduplication
                    source_key = (source_file, title)

                    # Only add if we haven't seen this source before
                    if source_key not in seen_sources:
                        seen_sources.add(source_key)

                        # Build context with title and source
                        context_parts.append(
                            f"[Source {source_number}]\n"
                            f"Title: {title}\n"
                            f"From: {source_file}\n\n"
                            f"{doc.page_content}"
                        )

                        # Track source for response metadata
                        sources_list.append(
                            {
                                "content": doc.page_content[:500],
                                "metadata": {
                                    "file_name": source_file,
                                    "document_title": title,
                                    "chunk_index": doc.metadata.get("chunk_index", 0),
                                },
                                "score": float(score),
                            }
                        )

                        source_number += 1

                context = "\n\n---\n\n".join(context_parts)

                # Store sources in state
                state["sources"] = sources_list

                # Add context as a system message
                context_message = SystemMessage(
                    content=(
                        f"RETRIEVED CONTEXT FROM KNOWLEDGE BASE:\n\n{context}\n\n"
                        "Instructions:\n"
                        "- Use this context to answer the user's question\n"
                        "- Be clear and concise\n"
                        "- The UI will automatically display source citations, so you don't need to list them"
                    )
                )
                messages = [context_message] + list(messages)

        # Return both messages and sources
        return {"messages": messages, "sources": state.get("sources", [])}

    async def _simple_agent(self, state: AgentState) -> AgentState:
        """
        Answer the question with RAG context already provided.

        Args:
            state: Current agent state with RAG context injected

        Returns:
            Updated state with answer
        """
        messages = state["messages"]

        # Add system message for simple mode
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            system_message = SystemMessage(
                content=(
                    "You are a knowledgeable AI assistant specializing in AI and Computing topics. "
                    "Context from the knowledge base has been provided above.\n\n"
                    "Instructions:\n"
                    "- Answer the question using the provided context\n"
                    "- Be clear and concise\n"
                    "- ALWAYS cite sources by number and title (e.g., 'Source 1: RAG Systems Overview')\n"
                    "- At the end of your answer, list: 'Sources used: Source 1 (title), Source 2 (title)...'\n"
                    "- If you need current/latest information, use the web search tool\n"
                    "- Keep responses focused and to-the-point"
                )
            )
            messages = [system_message] + list(messages)

        # Simple mode: Only web search tool available (RAG already done)
        from tools import create_web_search_tool

        web_tool = create_web_search_tool()
        simple_tools = [web_tool] if web_tool else []

        if simple_tools:
            llm_with_simple_tools = self.llm.bind_tools(simple_tools)
            response = await llm_with_simple_tools.ainvoke(messages)
        else:
            response = await self.llm.ainvoke(messages)

        # Preserve sources from state (populated by _simple_rag node)
        return {"messages": [response], "sources": state.get("sources", [])}

    async def _research_planner(self, state: AgentState) -> AgentState:
        """
        Research planning agent - breaks down the topic and plans research approach.

        Args:
            state: Current agent state

        Returns:
            Updated state with planning decision
        """
        messages = state["messages"]

        # Add planning system message
        system_message = SystemMessage(
            content=(
                "You are a Research Planning Agent. Your job is to break down research topics "
                "into manageable subtopics and create a research plan.\n\n"
                "Your task:\n"
                "1. Use 'research_topic_breakdown' tool to create a research plan\n"
                "2. Identify key areas to investigate\n"
                "3. List specific questions to answer\n\n"
                "Do NOT gather information yet - just plan the research approach."
            )
        )
        messages = [system_message] + list(messages)

        # Only give planning tool
        from tools import research_topic_breakdown

        planning_tools = [research_topic_breakdown]
        llm_with_planning = self.llm.bind_tools(planning_tools)

        response = await llm_with_planning.ainvoke(messages)
        return {"messages": [response]}

    async def _research_gatherer(self, state: AgentState) -> AgentState:
        """
        Research gathering agent - collects information from KB and web.

        Args:
            state: Current agent state with research plan

        Returns:
            Updated state with gathered information
        """
        messages = state["messages"]

        # Check if we need a system message
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            system_message = SystemMessage(
                content=(
                    "You are a Research Gathering Agent. You have a research plan. "
                    "Now gather comprehensive information.\n\n"
                    "Your task:\n"
                    "1. Use 'search_knowledge_base' to find foundational concepts\n"
                    "2. Use 'search_web' to find latest information and current trends\n"
                    "3. Gather information for each subtopic in your plan\n"
                    "4. For each source, extract key information and insights\n"
                    "5. Organize findings by topic/subtopic\n\n"
                    "When you have gathered sufficient sources (aim for 5+ KB sources and 5+ web sources), "
                    "summarize your findings briefly and say: 'RESEARCH COMPLETE - Ready to build report'\n\n"
                    "Keep your summary brief - the full report will be written in the next phase."
                )
            )
            messages = [system_message] + list(messages)

        # Give access to KB and web search tools
        from tools import create_web_search_tool, search_knowledge_base

        # Create a new web search tool instance for this request
        # Initialize it with the current counter from state
        web_search_tool = create_web_search_tool()
        if web_search_tool:
            web_search_tool.source_counter = state.get("web_source_counter", 0)

        gathering_tools = [search_knowledge_base]
        if web_search_tool:
            gathering_tools.append(web_search_tool.as_tool())

        llm_with_gathering = self.llm.bind_tools(gathering_tools)
        response = await llm_with_gathering.ainvoke(messages)

        # Update the counter in state for next search
        new_counter = web_search_tool.source_counter if web_search_tool else 0
        return {"messages": [response], "web_source_counter": new_counter}

    async def _report_builder(self, state: AgentState) -> AgentState:
        """
        Report building agent - synthesizes findings into a comprehensive report.

        Args:
            state: Current agent state with all gathered information

        Returns:
            Updated state with final report
        """
        messages = state["messages"]

        # Add report building system message
        system_message = SystemMessage(
            content=(
                "You are a Report Building Agent. You have gathered comprehensive research from multiple sources. "
                "Now synthesize ALL the gathered information into a detailed MARKDOWN report.\n\n"
                "IMPORTANT INSTRUCTIONS:\n"
                "1. Write a comprehensive, well-structured MARKDOWN report\n"
                "2. Use proper markdown formatting: # for title, ## for main sections, ### for subsections\n"
                "3. Create sections covering:\n"
                "   - Introduction/Overview\n"
                "   - Core concepts and definitions\n"
                "   - Historical context and evolution\n"
                "   - Current state and technologies\n"
                "   - Challenges and limitations\n"
                "   - Future trends\n"
                "   - Real-world applications\n"
                "   - Conclusion\n"
                "4. Cite sources inline using [KB-X] or [WEB-X] format where you use information\n"
                "5. Include a ## References section at the end with two subsections:\n"
                "   ### Knowledge Base Sources\n"
                "   [KB-1] Title (filename)\n"
                "   ### Web Sources\n"
                "   [WEB-1] Title (URL)\n"
                "6. DO NOT include any text after the References section\n"
                "7. DO NOT just list sources - write detailed explanatory content for each section\n"
                "8. Make it thorough and comprehensive - aim for 800+ words\n\n"
                "Write in an academic but accessible style. Be thorough and provide substantive content in each section."
            )
        )
        messages = [system_message] + list(messages)

        # Generate final report directly (no tools needed)
        response = await self.llm.ainvoke(messages)
        return {"messages": [response]}

    def _check_research_ready(self, state: AgentState) -> str:
        """
        Check if research gathering is complete or needs more information.

        Args:
            state: Current agent state

        Returns:
            "gather_more" or "build_report"
        """
        messages = state["messages"]
        last_message = messages[-1]

        # Check if gatherer signaled completion
        if isinstance(last_message, AIMessage):
            content = last_message.content.lower() if last_message.content else ""
            if "research complete" in content or "ready to build" in content:
                return "build_report"

            # Check if has tool calls (wants to gather more)
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "gather_more"

        # Default: assume ready to build after gathering
        return "build_report"

    async def _call_model(self, state: AgentState) -> AgentState:
        """
        Call the LLM with the current state.
        Note: For simple mode, RAG context is already injected by simple_rag node.

        Args:
            state: Current agent state

        Returns:
            Updated state with model response
        """
        messages = state["messages"]

        # Get routing decision
        mode = state.get("routing_decision", "simple")

        # Add system message if not present - tailored to mode
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            if mode == "research":
                # Deep research mode - uses tools for everything
                system_message = SystemMessage(
                    content=(
                        "You are a Deep Research Assistant specializing in AI and Computing topics. "
                        "Your mission is to conduct comprehensive research and write detailed, well-structured reports in MARKDOWN format.\n\n"
                        "RESEARCH WORKFLOW:\n"
                        "1. PLAN: Use 'research_topic_breakdown' to break down the topic into subtopics and key questions\n"
                        "2. GATHER: Search both knowledge base (established concepts) AND web (latest info)\n"
                        "   - Use 'search_knowledge_base' for foundational knowledge → Returns [KB-X] sources\n"
                        "   - Use 'tavily_search_results_json' for recent developments → Returns [WEB-X] sources with URLs\n"
                        "3. SYNTHESIZE: Combine findings from multiple sources, noting agreements and contradictions\n"
                        "4. STRUCTURE: Use 'create_report_outline' to organize your findings\n"
                        "5. WRITE: Generate a comprehensive MARKDOWN report with proper citations\n\n"
                        "CITATION & REFERENCES:\n"
                        "- When using knowledge base info, cite as: (KB-1), (KB-2), etc.\n"
                        "- When using web info, cite as: (WEB-1), (WEB-2), etc.\n"
                        "- Track ALL sources you use throughout your research\n"
                        "- END your report with a '## References' section listing:\n"
                        "  * Knowledge Base Sources: [KB-X] Title (source file)\n"
                        "  * Web Sources: [WEB-X] Title (URL)\n\n"
                        "REPORT QUALITY STANDARDS:\n"
                        "- Write in MARKDOWN format with proper headings (##, ###)\n"
                        "- Be comprehensive and thorough, covering multiple angles\n"
                        "- Always cite sources inline using (KB-X) or (WEB-X) format\n"
                        "- Include both historical context and current state\n"
                        "- Identify controversies, debates, or different perspectives\n"
                        "- Use clear section headings and logical structure\n"
                        "- Write in an academic but accessible style\n"
                        "- Conclude with key takeaways and future directions\n"
                        "- MUST include '## References' section at the end with all sources"
                    )
                )
            else:
                # Simple mode - RAG context already injected above
                system_message = SystemMessage(
                    content=(
                        "You are a knowledgeable AI assistant specializing in AI and Computing topics. "
                        "Context from the knowledge base has been provided above.\n\n"
                        "Instructions:\n"
                        "- Answer the question using the provided context\n"
                        "- Be clear and concise\n"
                        "- ALWAYS cite sources by number and title (e.g., 'Source 1: RAG Systems Overview')\n"
                        "- At the end of your answer, list: 'Sources used: Source 1 (title), Source 2 (title)...'\n"
                        "- If you need current/latest information, use the web search tool\n"
                        "- Keep responses focused and to-the-point"
                    )
                )
            messages = [system_message] + list(messages)

        # For simple mode, give access to web tool only (RAG already done)
        # For research mode, give access to all tools
        if mode == "simple":
            # Simple mode: Only web search tool available
            from tools import create_web_search_tool

            web_tool = create_web_search_tool()
            simple_tools = [web_tool] if web_tool else []

            if simple_tools:
                llm_with_simple_tools = self.llm.bind_tools(simple_tools)
                response = await llm_with_simple_tools.ainvoke(messages)
            else:
                # No tools available, just answer
                response = await self.llm.ainvoke(messages)
        else:
            # Research mode: All tools available
            response = await self.llm_with_tools.ainvoke(messages)

        return {"messages": [response]}

    def _should_continue(self, state: AgentState) -> str:
        """
        Determine whether to continue with tool calls or end.

        Args:
            state: Current agent state

        Returns:
            "continue" if there are tool calls, "end" otherwise
        """
        messages = state["messages"]
        last_message = messages[-1]

        # If there are tool calls, continue
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "continue"

        return "end"

    async def astream(self, messages: List[dict], session_id: str = None):
        """
        Stream responses from the agent with token-level streaming.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            session_id: Optional session ID for tracking

        Yields:
            Chunks of the response as tokens are generated
        """
        # Convert message dicts to LangChain message objects
        lc_messages = []
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))

        # Initialize state with web source counter starting at 0
        initial_state = {"messages": lc_messages, "sources": [], "web_source_counter": 0}

        # Use astream_events for token-level streaming (v2 API)
        routing_mode = None
        collected_sources = []

        # Track which phase we're in to filter streaming
        current_phase = "routing"  # routing -> gathering/rag -> responding

        async for event in self.graph.astream_events(initial_state, version="v2"):
            kind = event["event"]
            node_name = event.get("name", "")

            # Track phase transitions via node completions
            if kind == "on_chain_start":
                # Update phase when entering specific nodes
                if "simple_agent" in node_name or "report_builder" in node_name:
                    current_phase = "responding"
                elif "simple_rag" in node_name:
                    current_phase = "rag"

            # Capture routing decision from router node
            if kind == "on_chain_end":
                if "router" in node_name.lower() or node_name == "_route_request":
                    output = event.get("data", {}).get("output", {})
                    if isinstance(output, dict) and "routing_decision" in output:
                        routing_mode = output["routing_decision"]
                        current_phase = "gathering" if routing_mode == "research" else "rag"
                        yield {"type": "step", "content": routing_mode}

                # Capture sources from simple_rag node
                elif "simple_rag" in node_name.lower() or node_name == "_simple_rag":
                    output = event.get("data", {}).get("output", {})
                    if isinstance(output, dict) and "sources" in output:
                        collected_sources = output["sources"]

            # Stream tokens ONLY during the responding phase
            elif kind == "on_chat_model_stream" and current_phase == "responding":
                chunk = event["data"]["chunk"]
                if hasattr(chunk, "content") and chunk.content:
                    yield {"type": "token", "content": chunk.content}

        # Emit sources if any were collected
        if collected_sources:
            yield {"type": "sources", "sources": collected_sources}

        # Signal completion
        yield {"type": "done"}

    async def ainvoke(self, messages: List[dict], session_id: str = None) -> dict:
        """
        Invoke the agent and get a complete response.

        Args:
            messages: List of message dictionaries
            session_id: Optional session ID

        Returns:
            Dictionary with response and sources
        """
        # Convert messages
        lc_messages = []
        for msg in messages:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                lc_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                lc_messages.append(SystemMessage(content=msg["content"]))

        # Initialize state
        initial_state = {
            "messages": lc_messages,
            "sources": [],
            "routing_decision": "simple",  # Default, will be determined by router
        }

        # Run the graph
        result = await self.graph.ainvoke(initial_state)

        # Extract the final response
        final_message = result["messages"][-1]

        # Get sources from state (populated during simple mode RAG retrieval)
        sources = result.get("sources", [])

        return {
            "message": (
                final_message.content
                if isinstance(final_message, AIMessage)
                else str(final_message)
            ),
            "sources": sources,
        }


# Global agent instance
agent = RAGAgent()
