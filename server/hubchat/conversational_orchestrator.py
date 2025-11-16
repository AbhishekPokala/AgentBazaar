"""
Simple HubChat Orchestrator using Claude Agent SDK
Processes single queries and orchestrates agent execution
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


# Define invoke_agent tool that calls the FastAPI backend
@tool(
    name="invoke_agent",
    description="Execute a specific agent service via the FastAPI backend. This creates a task step and tracks costs. Use this to delegate work to specialized agents.",
    input_schema={
        "task_id": str,
        "agent_id": str,
        "subtask": str,
        "required_skills": list
    }
)
def invoke_agent_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    Tool for HubChat to invoke agents through the FastAPI backend.
    This ensures proper cost tracking and task lifecycle management.
    
    NOTE: Must be SYNC for Claude Agent SDK compatibility (no asyncio.run!)
    """
    task_id = args.get("task_id")
    agent_id = args.get("agent_id")
    subtask = args.get("subtask", "")
    required_skills = args.get("required_skills", [])

    logger.info(f"invoke_agent_tool called: task_id={task_id}, agent_id={agent_id}")

    if not all([task_id, agent_id, subtask]):
        return {
            "content": [{
                "type": "text",
                "text": "Error: Missing required parameters (task_id, agent_id, subtask)"
            }],
            "is_error": True
        }

    # Call the FastAPI backend using SYNC httpx.Client
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

    try:
        # Use synchronous httpx.Client (NOT AsyncClient)
        with httpx.Client(timeout=60.0) as client:
            # Only create a task if task_id is not provided
            if not task_id or task_id == "null" or task_id == "None":
                logger.info(f"Creating new task for: {subtask}")
                task_response = client.post(
                    f"{backend_url}/api/tasks",
                    json={
                        "userQuery": subtask,
                        "requiredSkills": required_skills if required_skills else [agent_id],
                        "status": "created",
                        "maxBudget": 10.0  # Default budget
                    }
                )

                if task_response.status_code in [200, 201]:
                    # Get the generated task_id from response
                    # API returns {"task": {...}} structure
                    task_data = task_response.json()
                    task_obj = task_data.get("task") or task_data  # Handle both structures
                    actual_task_id = task_obj.get("id")
                    logger.info(f"Task created with ID: {actual_task_id}")
                else:
                    logger.error(f"Failed to create task: {task_response.status_code} - {task_response.text}")
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"Error: Failed to create task - {task_response.text}"
                        }],
                        "is_error": True
                    }
            else:
                # Use the provided task_id
                actual_task_id = task_id
                logger.info(f"Using existing task ID: {actual_task_id}")

            # Now invoke the agent with the actual task_id
            payload = {
                "task_id": actual_task_id,
                "agent_id": agent_id,
                "subtask_type": subtask,
                "input_data": {"required_skills": required_skills} if required_skills else {}
            }

            logger.info(f"Calling FastAPI invoke endpoint: {backend_url}/api/invoke-agent")
            response = client.post(
                f"{backend_url}/api/invoke-agent",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()

        logger.info(f"Agent {agent_id} invoked successfully")
        
        # Format the response nicely and ALWAYS include the task_id
        if result.get("success"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"Agent {agent_id} completed successfully.\nResult: {result.get('result', 'N/A')}\nCost: ${result.get('cost', 0):.4f}"
                }],
                "task_id": actual_task_id  # Propagate task ID for tracking
            }
        else:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Agent {agent_id} failed: {result.get('error', 'Unknown error')}"
                }],
                "is_error": True,
                "task_id": actual_task_id  # Propagate task ID even on error
            }
            
    except Exception as e:
        logger.error(f"Error calling FastAPI invoke endpoint: {str(e)}", exc_info=True)
        return {
            "content": [{
                "type": "text",
                "text": f"Error invoking agent {agent_id}: {str(e)}"
            }],
            "is_error": True
        }


class ConversationalOrchestrator:
    """
    Simple orchestrator that processes single queries using Claude Agent SDK.
    Does not maintain conversation history - each query is independent.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the orchestrator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        logger.info("Initializing HubChat Orchestrator...")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        # Create MCP server with invoke_agent tool
        self.tools_server = create_sdk_mcp_server(
            name="agent_tools",
            tools=[invoke_agent_tool]
        )
        logger.info("Orchestrator initialized successfully")

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]] = None,
        task_id: Optional[str] = None,
        max_budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process a single user query using Claude Agent SDK.
        Does NOT use conversation history - each query is independent.

        Args:
            user_message: The user's query
            conversation_history: IGNORED - kept for API compatibility
            task_id: Optional task ID for linking
            max_budget: Optional maximum budget in USD

        Returns:
            Dict containing:
            - success: bool
            - response: str (orchestrator's response)
            - cost_breakdown: dict with cost information
            - task_id: str (if applicable)
        """
        logger.info(f"Processing single query (non-conversational): {user_message[:100]}...")
        
        # Configure Claude Agent SDK with tools
        # Tool naming format: mcp__{server_name}__{tool_name}
        # Server name: "agent_tools", Tool name: "invoke_agent"
        # Full identifier: "mcp__agent_tools__invoke_agent"
        options = ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            mcp_servers={"agent_tools": self.tools_server},
            allowed_tools=["mcp__agent_tools__invoke_agent"],
            permission_mode="bypassPermissions"
        )

        response_text = ""
        total_cost = 0.0
        agents_used = []

        try:
            # Use Claude Agent SDK to process the query
            # Pass API key explicitly to ClaudeSDKClient
            async with ClaudeSDKClient(api_key=self.api_key, options=options) as client:
                logger.info("Sending query to Claude Agent SDK...")
                
                # Send the user query
                await client.query(user_message)
                
                # Collect the response
                logger.info("Collecting response...")
                from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock
                
                async for message in client.receive_response():
                    # Handle AssistantMessage type from Claude Agent SDK
                    if isinstance(message, AssistantMessage):
                        for block in message.content:
                            # Collect text responses
                            if isinstance(block, TextBlock):
                                response_text += block.text
                                logger.debug(f"Collected text: {block.text[:50]}...")
                            
                            # Track tool usage (agent invocations)
                            elif isinstance(block, ToolUseBlock):
                                logger.info(f"Agent invoked: {block.name} with input {block.input}")
                                if 'invoke_agent' in block.name:
                                    agent_info = {
                                        "agent": block.input.get("agent_id", "unknown"),
                                        "task_id": block.input.get("task_id", task_id)
                                    }
                                    agents_used.append(agent_info)
                        
                        # Capture token usage for cost tracking
                        if hasattr(message, 'usage') and message.usage:
                            input_tokens = getattr(message.usage, 'input_tokens', 0)
                            output_tokens = getattr(message.usage, 'output_tokens', 0)
                            
                            # Calculate costs
                            input_cost = (input_tokens / 1_000_000) * 3.0
                            output_tokens_cost = (output_tokens / 1_000_000) * 15.0
                            total_cost += input_cost + output_tokens_cost
                            logger.info(f"Tokens: {input_tokens} in, {output_tokens} out | Cost: ${total_cost:.4f}")

                logger.info("Response collection complete")

            return {
                "success": True,
                "response": response_text.strip() if response_text else "Task completed successfully.",
                "cost_breakdown": {
                    "internal_cost": 0.0,
                    "external_cost": total_cost,
                    "total_cost": total_cost
                },
                "agents_used": agents_used,
                "task_id": task_id
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            return {
                "success": False,
                "response": f"I encountered an error: {str(e)}",
                "cost_breakdown": {
                    "internal_cost": 0.0,
                    "external_cost": 0.0,
                    "total_cost": 0.0
                },
                "agents_used": [],
                "task_id": task_id
            }
