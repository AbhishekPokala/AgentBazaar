"""
Tool definitions for HubChat to interact with agents directly.
These tools are exposed to the Anthropic Agent SDK.
"""

import os
import httpx
from typing import Any, Dict, List, Optional
from anthropic.types.beta import BetaToolUnionParam

# Agent service URLs
AGENT_URLS = {
    "summarizer": os.getenv("SUMMARIZER_URL", "http://localhost:8001"),
    "translator": os.getenv("TRANSLATOR_URL", "http://localhost:8002"),
    "search": os.getenv("SEARCH_URL", "http://localhost:8003"),
    "mock_busy": os.getenv("MOCK_BUSY_URL", "http://localhost:8004"),
    "mock_highprice": os.getenv("MOCK_HIGHPRICE_URL", "http://localhost:8005"),
    "mock_negotiator": os.getenv("MOCK_NEGOTIATOR_URL", "http://localhost:8006"),
}


# Simplified tool definitions - directly call agents
TOOLS: List[BetaToolUnionParam] = [
    {
        "name": "invoke_agent",
        "description": "Execute a specific agent with the given payload. Returns the agent's result, cost, and metadata. Available agents: summarizer, translator, search, mock_busy, mock_highprice, mock_negotiator.",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_id": {
                    "type": "string",
                    "description": "The ID of the agent to invoke (summarizer, translator, search, etc.)"
                },
                "payload": {
                    "type": "object",
                    "description": "The input data for the agent"
                }
            },
            "required": ["agent_id", "payload"]
        }
    }
]


class ToolExecutor:
    """Executes tool calls by making HTTP requests directly to agent services."""

    def __init__(self):
        self.client = httpx.Client(timeout=30.0)

    async def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call and return the result."""

        if tool_name == "invoke_agent":
            return await self._invoke_agent(tool_input)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    async def _invoke_agent(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call agent's /execute endpoint directly"""
        try:
            agent_id = input_data.get("agent_id")
            payload = input_data.get("payload", {})

            # Get agent URL
            if agent_id not in AGENT_URLS:
                return {"error": f"Unknown agent: {agent_id}. Available: {list(AGENT_URLS.keys())}"}

            agent_url = AGENT_URLS[agent_id]

            # Call agent's /execute endpoint
            response = self.client.post(
                f"{agent_url}/execute",
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            # Add agent_id to response for tracking
            result["agent_id"] = agent_id

            return result

        except httpx.HTTPStatusError as e:
            return {
                "error": f"Agent returned error: {e.response.status_code}",
                "detail": e.response.text
            }
        except Exception as e:
            return {"error": f"Failed to call agent: {str(e)}"}

    def close(self):
        """Close the HTTP client."""
        self.client.close()

