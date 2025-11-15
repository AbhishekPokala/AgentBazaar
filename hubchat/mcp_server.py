"""
HubChat MCP Server using FastMCP
Exposes HubChat orchestrator as MCP tools for ChatGPT Desktop
"""

import asyncio
import os
import logging
from typing import Optional
from fastmcp import FastMCP

# Import HubChat orchestrator
try:
    from orchestrator import process_request
except ImportError:
    from hubchat.orchestrator import process_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("HubChat Orchestrator")


@mcp.tool()
async def orchestrate_task(query: str, max_budget: Optional[float] = None) -> str:
    """
    Coordinate multiple AI agents to complete a complex task.

    This tool acts as a central orchestrator that:
    - Understands your request
    - Plans which specialized agents to use
    - Coordinates multiple agents if needed (e.g., summarize then translate)
    - Returns aggregated results with cost breakdown

    Available agents:
    - Summarizer: Text summarization and condensing
    - Translator: Language translation
    - Search: Web search with synthesis

    Args:
        query: Natural language description of the task
               Examples:
               - "Translate 'Hello World' to Spanish"
               - "Summarize this text: [long text]"
               - "Search for Claude AI and summarize the results"
               - "Translate this to French then summarize it: [text]"
        max_budget: Optional maximum budget in USD (default: no limit)

    Returns:
        A formatted string with:
        - The final result
        - Which agents were used
        - Cost breakdown
        - Success status
    """
    logger.info(f"MCP tool called: orchestrate_task(query={query[:100]}...)")

    try:
        # Call HubChat orchestrator
        result = await process_request(
            user_query=query,
            max_budget=max_budget
        )

        # Format response
        success = result.get("success", False)
        output = result.get("output", "")
        cost_breakdown = result.get("cost_breakdown", {})
        agents_discovered = result.get("agents_discovered", [])
        agents_used = result.get("agents_used", [])
        payments_made = result.get("payments_made", [])
        total_paid = result.get("total_paid", 0.0)

        # Build formatted response
        response_parts = []

        # Status
        status_emoji = "✅" if success else "❌"
        response_parts.append(f"{status_emoji} **Status**: {'Success' if success else 'Failed'}")
        response_parts.append("")

        # Output
        response_parts.append("**Result:**")
        response_parts.append(output)
        response_parts.append("")

        # Discovery phase
        if agents_discovered:
            response_parts.append("**🔍 Agent Discovery:**")
            for discovery in agents_discovered:
                skill = discovery.get("skill", "unknown")
                max_price = discovery.get("max_price")
                price_str = f" (max ${max_price})" if max_price else ""
                response_parts.append(f"  - Searched for: {skill}{price_str}")
        response_parts.append("")

        # Agents used
        if agents_used:
            response_parts.append("**🤖 Agents Executed:**")
            for agent_info in agents_used:
                agent_name = agent_info.get("agent", "unknown")
                response_parts.append(f"  - {agent_name}")
            response_parts.append("")

        # Payments made
        if payments_made:
            response_parts.append("**💰 Payments Made (Locus):**")
            for payment in payments_made:
                agent_id = payment.get("agent_id", "unknown")
                amount = payment.get("amount", 0.0)
                memo = payment.get("memo", "")
                recipient = payment.get("recipient", "")
                response_parts.append(f"  - {agent_id}: ${amount:.2f} USDC → {recipient[:10]}...{recipient[-6:]}")
                if memo:
                    response_parts.append(f"    Memo: {memo}")
            response_parts.append(f"  - **Total Paid**: ${total_paid:.2f} USDC")
            response_parts.append("")

        # Cost breakdown
        internal_cost = cost_breakdown.get("internal_cost", 0.0)
        external_cost = cost_breakdown.get("external_cost", 0.0)
        total_cost = cost_breakdown.get("total_cost", 0.0)

        response_parts.append("**Cost Breakdown:**")
        response_parts.append(f"  - Internal (agents): ${internal_cost:.4f}")
        response_parts.append(f"  - External (APIs): ${external_cost:.4f}")
        response_parts.append(f"  - **Total**: ${total_cost:.4f}")

        formatted_response = "\n".join(response_parts)
        logger.info(f"Task completed successfully. Cost: ${total_cost:.4f}, Paid: ${total_paid:.2f}")

        return formatted_response

    except Exception as e:
        error_msg = f"❌ Error processing task: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg


@mcp.tool()
async def list_available_agents() -> str:
    """
    List all available specialized agents and their capabilities.

    Returns information about each agent including:
    - Agent ID and name
    - Skills/capabilities
    - Base pricing
    - Description
    """
    agents_info = [
        {
            "id": "summarizer",
            "name": "Summarizer Agent",
            "skills": ["summarize", "condense", "analyze"],
            "base_price": 0.05,
            "description": "Intelligent text summarization with configurable length"
        },
        {
            "id": "translator",
            "name": "Translator Agent",
            "skills": ["translate"],
            "base_price": 0.10,
            "description": "Language translation powered by Claude"
        },
        {
            "id": "search",
            "name": "Search Agent",
            "skills": ["search", "research", "web"],
            "base_price": 0.08,
            "description": "Web search with AI synthesis of results"
        }
    ]

    response_parts = ["**Available AI Agents:**\n"]

    for agent in agents_info:
        response_parts.append(f"### {agent['name']} (`{agent['id']}`)")
        response_parts.append(f"**Description:** {agent['description']}")
        response_parts.append(f"**Skills:** {', '.join(agent['skills'])}")
        response_parts.append(f"**Base Price:** ${agent['base_price']:.2f}")
        response_parts.append("")

    response_parts.append("\n**How to use:**")
    response_parts.append("Use the `orchestrate_task` tool with a natural language query.")
    response_parts.append("The orchestrator will automatically select the right agent(s).")

    return "\n".join(response_parts)


@mcp.resource("hubchat://status")
async def get_status() -> str:
    """
    Get the current status of the HubChat orchestrator and available agents.
    """
    return """
    HubChat Orchestrator - Status
    ==============================

    Status: ✅ Online

    Available Tools:
    - orchestrate_task: Coordinate multiple AI agents
    - list_available_agents: View agent capabilities

    Available Agents:
    - Summarizer (text summarization)
    - Translator (language translation)
    - Search (web search + synthesis)

    How to use:
    Simply describe what you want in natural language, and HubChat
    will automatically coordinate the appropriate agents to complete
    your task.

    Examples:
    - "Translate 'Hello' to Spanish"
    - "Summarize this article: [text]"
    - "Search for Claude AI and tell me about it"
    - "Translate to French and then summarize: [text]"
    """


@mcp.prompt()
async def multi_agent_workflow() -> str:
    """
    Example prompt showing how to use HubChat for multi-step tasks.
    """
    return """
    You are working with HubChat, a multi-agent orchestration system.

    HubChat can coordinate multiple specialized AI agents to complete complex tasks:
    - Summarizer: Condense long text
    - Translator: Translate between languages
    - Search: Find and synthesize information from the web

    When a user asks you to:
    1. Summarize or condense text
    2. Translate to another language
    3. Search for information
    4. Perform multi-step tasks (e.g., search then summarize, translate then summarize)

    Use the orchestrate_task tool with a clear natural language query.

    Examples:
    - User: "Summarize this article and translate to Spanish: [text]"
      Tool: orchestrate_task(query="Summarize and translate to Spanish: [text]")

    - User: "What's the latest on SpaceX?"
      Tool: orchestrate_task(query="Search for latest SpaceX news and summarize")

    Always show the user:
    - The final result
    - Which agents were used
    - The cost breakdown
    """


def main():
    """Run the MCP server"""
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        return

    logger.info("=" * 60)
    logger.info("🚀 Starting HubChat MCP Server")
    logger.info("=" * 60)
    logger.info("Server: HubChat Orchestrator")
    logger.info("Protocol: Model Context Protocol (MCP)")
    logger.info("Tools: orchestrate_task, list_available_agents")
    logger.info("Resources: hubchat://status")
    logger.info("=" * 60)
    logger.info("")
    logger.info("⚠️  Make sure agents are running!")
    logger.info("   Run: ./start_all_services.sh")
    logger.info("")
    logger.info("💡 Add to ChatGPT Desktop config:")
    logger.info("   See MCP_SETUP.md for instructions")
    logger.info("")

    # Run the MCP server
    mcp.run(transport="http", host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()

