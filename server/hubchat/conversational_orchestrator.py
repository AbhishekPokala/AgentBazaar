"""
Conversational HubChat Orchestrator
Maintains conversation context across multiple turns
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
async def invoke_agent_tool(args: dict[str, Any]) -> dict[str, Any]:
    """
    Tool for HubChat to invoke agents through the FastAPI backend.
    This ensures proper cost tracking and task lifecycle management.
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

    # Call the FastAPI backend
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # First, create the task (or get existing one)
            logger.info(f"Creating task for: {subtask}")
            task_response = await client.post(
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
                task_data = task_response.json()
                actual_task_id = task_data.get("id")
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

            # Now invoke the agent with the actual task_id
            payload = {
                "task_id": actual_task_id,
                "agent_id": agent_id,
                "subtask_type": subtask,
                "input_data": {"required_skills": required_skills} if required_skills else {}
            }

            logger.info(f"Calling FastAPI invoke endpoint: {backend_url}/api/invoke-agent")
            response = await client.post(
                f"{backend_url}/api/invoke-agent",
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()

        logger.info(f"Agent {agent_id} invoked successfully")
        
        # Format the response nicely
        if result.get("success"):
            return {
                "content": [{
                    "type": "text",
                    "text": f"Agent {agent_id} completed successfully.\nResult: {result.get('result', 'N/A')}\nCost: ${result.get('cost', 0):.4f}"
                }]
            }
        else:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Agent {agent_id} failed: {result.get('error', 'Unknown error')}"
                }],
                "is_error": True
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
    Conversational orchestrator that maintains context across multiple turns.
    Uses Claude Agent SDK with conversation history for context retention.
    """

    def __init__(self, api_key: str[Optional] = ""):
        """
        Initialize the conversational orchestrator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        logger.info("Initializing ConversationalOrchestrator...")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        logger.info("Creating MCP server with invoke_agent tool...")
        # Create MCP server with invoke_agent tool
        self.tools_server = create_sdk_mcp_server(
            name="agent_tools",
            tools=[invoke_agent_tool]
        )
        logger.info("ConversationalOrchestrator initialized successfully")

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        task_id: Optional[str] = None,
        max_budget: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process a user message with full conversation context.

        Args:
            user_message: The new user message
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            task_id: Optional task ID for linking messages to tasks
            max_budget: Optional maximum budget in USD

        Returns:
            Dict containing:
            - success: bool
            - response: str (assistant's response)
            - cost_breakdown: dict with cost information
            - task_id: str (if applicable)
        """
        logger.info(f"Processing message with {len(conversation_history)} previous messages")
        
        # Build the conversation with context
        messages = []
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add the new user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Add budget context if provided
        if max_budget:
            messages[-1]["content"] += f"\n\n(Max budget: ${max_budget:.2f})"
        
        # Add task_id context if provided
        if task_id:
            messages[-1]["content"] += f"\n\n(Task ID: {task_id})"

        # Configure Claude with Agent SDK
        logger.info("Configuring ClaudeAgentOptions...")
        options = ClaudeAgentOptions(
            system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
            mcp_servers={"agents": self.tools_server},
            allowed_tools=["mcp__agents__invoke_agent"],
            permission_mode="bypassPermissions"
        )

        # Process with full conversation context
        response_text = ""
        total_cost = 0.0
        agents_used = []

        try:
            logger.info("Creating ClaudeSDKClient...")
            async with ClaudeSDKClient(options=options) as client:
                # Send all messages (full context)
                logger.info(f"Sending {len(messages)} messages to Claude...")
                for msg in messages:
                    if msg["role"] == "user":
                        await client.query(msg["content"])

                logger.info("Collecting response...")
                # Collect the assistant's response
                async for message in client.receive_response():
                    if hasattr(message, 'content'):
                        for block in message.content:
                            # Collect text
                            if hasattr(block, 'text'):
                                response_text += block.text
                                logger.debug(f"Collected text: {block.text[:50]}...")

                            # Track tool usage (agent invocations)
                            if hasattr(block, 'name') and block.name == "mcp__agents__invoke_agent":
                                logger.info(f"Agent invoked: {block.input.get('agent_id', 'unknown')}")
                                agent_info = {
                                    "agent": block.input.get("agent_id", "unknown"),
                                    "task_id": block.input.get("task_id", task_id)
                                }
                                agents_used.append(agent_info)

                logger.info("Response collection complete")

            return {
                "success": True,
                "response": response_text.strip(),
                "cost_breakdown": {
                    "internal_cost": total_cost,
                    "external_cost": 0.0,
                    "total_cost": total_cost
                },
                "agents_used": agents_used,
                "task_id": task_id
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
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
