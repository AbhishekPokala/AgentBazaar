"""
HubChat Orchestrator - Uses Official Claude Agent SDK
Central orchestrator that coordinates multiple agents
"""

import os
import sys
import json
import logging
from typing import Any, Dict, List, Optional
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, tool, create_sdk_mcp_server
import httpx

# Import Locus Client and Agent Registry
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from locus_test.locus_client import LocusClient

try:
    from .agent_registry import registry
except ImportError:
    from agent_registry import registry

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

# Locus Payment Configuration
LOCUS_CUSTOMER_API_KEY = "locus_dev_iP5FvYpYL7sm5ncGRqurxWkpYqHBBIZD"  # Customer_1 pays vendors
VENDOR_WALLET_ADDRESS = "0xe1e1d4503105d4b0466419ff173900031e7e5ed6"  # Vendor wallet

# Initialize Locus client
try:
    locus_client = LocusClient(LOCUS_CUSTOMER_API_KEY)
    logger.info("✅ Locus payment client initialized")
except Exception as e:
    logger.warning(f"⚠️  Locus client initialization failed: {e}")
    locus_client = None


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


@tool(
    name="discover_agents",
    description="Discover and compare available agents based on skills, cost, and reviews. Use this BEFORE invoking agents to find the best option.",
    input_schema={
        "skill": str,
        "max_price": float
    }
)
async def discover_agents_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    Tool for discovering agents by skill.
    Returns list of agents with pricing, ratings, and reviews.
    """
    skill = args.get("skill", "")
    max_price = args.get("max_price")

    logger.info(f"discover_agents_tool called: skill='{skill}', max_price=${max_price}")

    if not skill:
        return {
            "content": [{
                "type": "text",
                "text": "Error: Skill parameter is required"
            }],
            "is_error": True
        }

    try:
        # Discover agents matching the skill
        agents = registry.discover_by_skill(skill, max_price)

        if not agents:
            return {
                "content": [{
                    "type": "text",
                    "text": f"No agents found for skill '{skill}' within budget"
                }],
                "is_error": False
            }

        # Format agent information
        result = {
            "skill": skill,
            "agents_found": len(agents),
            "agents": []
        }

        for agent in agents:
            result["agents"].append({
                "id": agent["id"],
                "name": agent["name"],
                "description": agent["description"],
                "price": agent["base_price"],
                "rating": agent["rating"],
                "reviews": agent["total_reviews"],
                "success_rate": agent["success_rate"],
                "available": agent.get("available", True)
            })

        # Recommend best agent
        best = agents[0] if agents else None
        if best:
            result["recommended"] = best["id"]
            result["recommended_reason"] = f"Best rating ({best['rating']}★) at ${best['base_price']}"

        logger.info(f"Discovered {len(agents)} agents for '{skill}', recommending: {result.get('recommended')}")

        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, indent=2)
            }]
        }

    except Exception as e:
        logger.error(f"Error discovering agents: {str(e)}", exc_info=True)
        return {
            "content": [{
                "type": "text",
                "text": f"Error discovering agents: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    name="make_payment",
    description="Process a payment via Locus blockchain to a specific agent's wallet. Use this after an agent successfully completes a task. Specify the agent_id so payment goes to the correct agent.",
    input_schema={
        "agent_id": str,
        "amount": float,
        "memo": str
    }
)
async def make_payment_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    Tool for processing payments via Locus.
    Sends USDC from customer wallet to specific agent's wallet.
    """
    agent_id = args.get("agent_id", "")
    amount = args.get("amount", 0.0)
    memo = args.get("memo", "Agent service payment")

    logger.info(f"make_payment_tool called: agent_id='{agent_id}', amount=${amount}, memo='{memo}'")

    if not locus_client:
        logger.error("Locus client not initialized")
        return {
            "content": [{
                "type": "text",
                "text": "Error: Payment system not available"
            }],
            "is_error": True
        }

    if amount <= 0:
        logger.error(f"Invalid amount: {amount}")
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Invalid payment amount: ${amount}"
            }],
            "is_error": True
        }

    # Get agent's wallet address from registry
    agent_info = registry.get_agent_by_id(agent_id)
    if not agent_info:
        logger.error(f"Agent not found: {agent_id}")
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Agent '{agent_id}' not found in registry"
            }],
            "is_error": True
        }

    wallet_address = agent_info.get("wallet_address")
    if not wallet_address:
        logger.error(f"No wallet address for agent: {agent_id}")
        return {
            "content": [{
                "type": "text",
                "text": f"Error: No wallet configured for agent '{agent_id}'"
            }],
            "is_error": True
        }

    try:
        logger.info(f"Processing payment: ${amount} to {agent_id} wallet {wallet_address}")
        result = locus_client.send_to_address(
            address=wallet_address,
            amount=amount,
            memo=memo
        )

        success = result.get("success", False)
        message = result.get("message", "Payment processed")

        logger.info(f"Payment result: {success}, message: {message}")

        return {
            "content": [{
                "type": "text",
                "text": json.dumps({
                    "payment_success": success,
                    "agent_id": agent_id,
                    "amount": amount,
                    "recipient": wallet_address,
                    "memo": memo,
                    "message": message
                }, indent=2)
            }],
            "is_error": not success
        }

    except Exception as e:
        logger.error(f"Payment error: {str(e)}", exc_info=True)
        return {
            "content": [{
                "type": "text",
                "text": f"Error processing payment: {str(e)}"
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

        logger.info("Creating MCP server with discovery, invoke, and payment tools...")
        # Create MCP server with all tools: discovery, invoke, payment
        self.tools_server = create_sdk_mcp_server(
            name="agent_tools",
            tools=[discover_agents_tool, invoke_agent_tool, make_payment_tool]
        )
        logger.info("HubChatOrchestrator initialized successfully (with agent discovery & Locus payments)")

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
            allowed_tools=[
                "mcp__agents__discover_agents",
                "mcp__agents__invoke_agent",
                "mcp__agents__make_payment"
            ],
            permission_mode="bypassPermissions"
        )

        # Use ClaudeSDKClient for conversation with tool calling
        result_text = ""
        agents_discovered = []
        agents_used = []
        payments_made = []
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
                            if hasattr(block, 'name'):
                                if block.name == "mcp__agents__discover_agents":
                                    # Agent discovery
                                    skill = block.input.get("skill", "unknown")
                                    max_price = block.input.get("max_price")
                                    logger.info(f"Agents discovered for skill: {skill} (max_price: ${max_price})")
                                    agents_discovered.append({
                                        "skill": skill,
                                        "max_price": max_price
                                    })

                                elif block.name == "mcp__agents__invoke_agent":
                                    # Agent was invoked
                                    logger.info(f"Agent invoked: {block.input.get('agent_id', 'unknown')}")
                                    agent_info = {
                                        "agent": block.input.get("agent_id", "unknown"),
                                        "payload": block.input.get("payload", {})
                                    }
                                    agents_used.append(agent_info)

                                elif block.name == "mcp__agents__make_payment":
                                    # Payment was made
                                    agent_id = block.input.get("agent_id", "unknown")
                                    amount = block.input.get("amount", 0.0)
                                    memo = block.input.get("memo", "")
                                    logger.info(f"Payment made: ${amount} to {agent_id} - {memo}")

                                    # Get agent wallet from registry
                                    agent = registry.get_agent_by_id(agent_id)
                                    wallet = agent.get("wallet_address", "unknown") if agent else "unknown"

                                    payment_info = {
                                        "agent_id": agent_id,
                                        "amount": amount,
                                        "memo": memo,
                                        "recipient": wallet
                                    }
                                    payments_made.append(payment_info)
                                    total_cost += amount

                logger.info("Response collection complete")

            return {
                "success": True,
                "output": result_text.strip(),
                "cost_breakdown": {
                    "internal_cost": total_cost,
                    "external_cost": 0.0,
                    "total_cost": total_cost
                },
                "agents_discovered": agents_discovered,
                "agents_used": agents_used,
                "payments_made": payments_made,
                "total_paid": sum(p["amount"] for p in payments_made)
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
                "agents_discovered": [],
                "agents_used": [],
                "payments_made": [],
                "total_paid": 0.0
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
