"""
Search Agent - Uses Official Claude Agent SDK with custom tools
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server
)
from typing import Any
import json

app = FastAPI(title="Search Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    query: str
    num_results: int = 5


class ExecuteResponse(BaseModel):
    """Uniform response format"""
    result: str
    cost: float
    subtask_type: str
    requires_external_tool: bool
    external_cost: float


# Define custom web_search tool using @tool decorator from Claude Agent SDK
@tool(
    name="web_search",
    description="Search the web for information. Returns search results with titles, URLs, and snippets.",
    input_schema={
        "query": str,
        "num_results": int
    }
)
async def web_search(args: dict[str, Any]) -> dict[str, Any]:
    """
    Web search tool implementation.
    In production, call real search API (Brave, Serper, etc.)
    """
    query = args.get("query", "")
    num_results = args.get("num_results", 5)

    # Mock search results - replace with real API
    results = [
        {
            "title": f"Result {i+1}: {query}",
            "url": f"https://example.com/{query.replace(' ', '-')}-{i+1}",
            "snippet": f"This source discusses {query} with detailed information. "
                      f"Contains analysis and relevant data points from perspective {i+1}."
        }
        for i in range(num_results)
    ]

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(results, indent=2)
        }]
    }


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """
    Execute web search using Claude Agent SDK with custom tools.

    The agent will:
    1. Use web_search tool to find information
    2. Analyze results
    3. Synthesize answer with citations
    """
    try:
        # Create SDK MCP server with web_search tool
        search_server = create_sdk_mcp_server(
            name="search_tools",
            tools=[web_search]
        )

        # Configure agent with Claude Agent SDK
        options = ClaudeAgentOptions(
            system_prompt="""You are an autonomous search and research agent.

Your capabilities:
- Use the web_search tool to find information
- Analyze search results critically
- Synthesize comprehensive answers from multiple sources
- Provide citations with [1], [2], etc.

Workflow:
1. Use web_search to find relevant information
2. Analyze the quality and relevance of results
3. Synthesize a well-structured answer
4. Cite all sources at the end

Be thorough and accurate.""",
            mcp_servers={"search": search_server},
            allowed_tools=["mcp__search__web_search"],
            permission_mode="bypassPermissions"
        )

        # Use ClaudeSDKClient for tool-based interaction
        result_text = ""
        search_api_cost = 0.01 * request.num_results

        async with ClaudeSDKClient(options=options) as client:
            # Send search query
            await client.query(
                f"Search for information about: {request.query}. "
                f"Use the web_search tool with query='{request.query}' and num_results={request.num_results}. "
                f"Then synthesize the findings into a comprehensive answer with citations."
            )

            # Collect response
            async for message in client.receive_response():
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            result_text += block.text

        # Estimate internal cost
        estimated_internal_cost = 0.08 + (len(request.query) / 100) * 0.02

        return ExecuteResponse(
            result=result_text.strip(),
            cost=round(estimated_internal_cost, 2),
            subtask_type="search",
            requires_external_tool=True,
            external_cost=round(search_api_cost, 2)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "search",
        "powered_by": "Claude Agent SDK (Official)",
        "framework": "claude-agent-sdk",
        "capabilities": ["web_search", "tool_calling", "synthesis"]
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Search Agent",
        "description": "Web search and synthesis using official Claude Agent SDK with custom tools",
        "skills": ["search", "research", "synthesis", "citation"],
        "base_price": 0.08,
        "agent_type": "claude_agent_sdk_with_tools",
        "framework": "claude-agent-sdk",
        "tools": ["web_search"]
    }


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        exit(1)

    uvicorn.run(app, host="0.0.0.0", port=8003)
