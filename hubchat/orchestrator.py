"""
HubChat Orchestrator - Uses Official Claude Agent SDK
Central orchestrator that coordinates multiple agents
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, tool, create_sdk_mcp_server
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from .prompts import ORCHESTRATOR_SYSTEM_PROMPT
except ImportError:
    from prompts import ORCHESTRATOR_SYSTEM_PROMPT

# Agent service URLs
AGENT_URLS = {
    "summarizer": os.getenv("SUMMARIZER_URL", "http://localhost:8001"),
    "translator": os.getenv("TRANSLATOR_URL", "http://localhost:8002"),
    "search": os.getenv("SEARCH_URL", "http://localhost:8003"),
}


# Define invoke_agent tool for HubChat using Claude Agent SDK @tool decorator
@tool(
    name="invoke_agent",
    description="Execute a specific agent service. Available agents: summarizer, translator, search. Each agent has specific input requirements.",
    input_schema={
        "agent_id": str,
        "payload": dict
    }
)
async def invoke_agent_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    Tool for HubChat to invoke other agents.
    """
    agent_id = args.get("agent_id")
    payload = args.get("payload", {})

    logger.info(f"invoke_agent_tool called: agent_id={agent_id}, payload={payload}, payload_type={type(payload)}")

    # If payload is a string, parse it as JSON
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
            logger.info(f"Parsed payload from string to dict: {payload}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse payload JSON: {e}")
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error: Invalid JSON payload: {str(e)}"
                }],
                "is_error": True
            }

    if agent_id not in AGENT_URLS:
        logger.warning(f"Unknown agent: {agent_id}")
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Unknown agent '{agent_id}'. Available: {list(AGENT_URLS.keys())}"
            }],
            "is_error": True
        }

    agent_url = AGENT_URLS[agent_id]
    logger.info(f"Calling agent at {agent_url}/execute")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            logger.info(f"Sending payload to {agent_id}: {json.dumps(payload, indent=2)}")
            response = await client.post(f"{agent_url}/execute", json=payload)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code != 200:
                logger.error(f"Error response from {agent_id}: {response.text}")

            response.raise_for_status()
            result = response.json()

        logger.info(f"Agent {agent_id} responded successfully: {json.dumps(result, indent=2)[:200]}...")
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, indent=2)
            }]
        }
    except Exception as e:
        logger.error(f"Error calling agent {agent_id}: {str(e)}", exc_info=True)
        return {
            "content": [{
                "type": "text",
                "text": f"Error calling {agent_id}: {str(e)}"
            }],
            "is_error": True
        }


class HubChatOrchestrator:
    """
    Central orchestrator using Official Claude Agent SDK.
    Coordinates multiple specialized agents to complete complex tasks.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the orchestrator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        logger.info("Initializing HubChatOrchestrator...")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        logger.info("Creating MCP server with invoke_agent tool...")
        # Create MCP server with invoke_agent tool
        self.tools_server = create_sdk_mcp_server(
            name="agent_tools",
            tools=[invoke_agent_tool]
        )
        logger.info("HubChatOrchestrator initialized successfully")

    async def process_user_request(
        self,
        user_query: str,
        max_budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process a user request using Claude Agent SDK.

        HubChat will autonomously:
        - Understand the request
        - Decide which agents to use
        - Invoke agents via invoke_agent tool
        - Aggregate results

        Args:
            user_query: User's natural language request
            max_budget: Optional maximum budget in USD

        Returns:
            Dict containing the final result and cost breakdown
        """
        # Build prompt
        logger.info(f"Processing user query: {user_query[:100]}...")
        prompt = user_query
        if max_budget:
            prompt += f"\n\n(Max budget: ${max_budget:.2f})"

        # Configure HubChat with Claude Agent SDK
        logger.info("Configuring ClaudeAgentOptions...")
        options = ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            mcp_servers={"agents": self.tools_server},
            allowed_tools=["mcp__agents__invoke_agent"],
            permission_mode="bypassPermissions"
        )

        # Use ClaudeSDKClient for conversation with tool calling
        result_text = ""
        agents_used = []
        total_cost = 0.0

        try:
            logger.info("Creating ClaudeSDKClient...")
            async with ClaudeSDKClient(options=options) as client:
                logger.info("Sending query to Claude...")
                await client.query(prompt)

                logger.info("Collecting response...")
                # Collect response and track tool usage
                async for message in client.receive_response():
                    logger.debug(f"Received message type: {type(message)}")
                    if hasattr(message, 'content'):
                        for block in message.content:
                            # Collect text
                            if hasattr(block, 'text'):
                                result_text += block.text
                                logger.debug(f"Collected text: {block.text[:50]}...")

                            # Track tool usage
                            if hasattr(block, 'name') and block.name == "mcp__agents__invoke_agent":
                                # Agent was invoked
                                logger.info(f"Agent invoked: {block.input.get('agent_id', 'unknown')}")
                                agent_info = {
                                    "agent": block.input.get("agent_id", "unknown"),
                                    "payload": block.input.get("payload", {})
                                }
                                agents_used.append(agent_info)

                logger.info("Response collection complete")

            return {
                "success": True,
                "output": result_text.strip(),
                "cost_breakdown": {
                    "internal_cost": total_cost,
                    "external_cost": 0.0,
                    "total_cost": total_cost
                },
                "agents_used": agents_used
            }

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return {
                "success": False,
                "output": f"Error: {str(e)}",
                "cost_breakdown": {
                    "internal_cost": 0.0,
                    "external_cost": 0.0,
                    "total_cost": 0.0
                },
                "agents_used": []
            }


# Convenience function for single-turn interactions
async def process_request(
    user_query: str,
    max_budget: Optional[float] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a single user request using Claude Agent SDK.

    Args:
        user_query: User's natural language request
        max_budget: Optional maximum budget in USD
        api_key: Anthropic API key (defaults to env var)

    Returns:
        Dict containing the final result and cost breakdown
    """
    logger.info("process_request() called")
    orchestrator = HubChatOrchestrator(api_key=api_key)
    logger.info("Calling orchestrator.process_user_request()...")
    result = await orchestrator.process_user_request(user_query, max_budget)
    logger.info("process_request() completed")
    return result
