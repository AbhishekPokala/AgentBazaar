"""
Summarizer Agent - Uses Official Claude Agent SDK
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn
from claude_agent_sdk import query, ClaudeAgentOptions

app = FastAPI(title="Summarizer Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    text: str
    max_length: int = 100


class ExecuteResponse(BaseModel):
    """Uniform response format"""
    result: str
    cost: float
    subtask_type: str
    requires_external_tool: bool
    external_cost: float


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """
    Execute text summarization using Claude Agent SDK.
    """
    try:
        # Configure agent with Claude Agent SDK
        options = ClaudeAgentOptions(
            system_prompt=f"""You are an expert text summarization agent.

Task: Summarize the provided text in approximately {request.max_length} characters.

Guidelines:
- Extract the most important information
- Be concise and accurate
- Maintain key facts and main ideas
- Don't add information not in the original

Provide only the summary, no explanations.""",
            allowed_tools=[],  # No tools needed for summarization
            permission_mode="bypassPermissions"
        )

        # Use Claude Agent SDK query() function
        result_text = ""
        async for message in query(
            prompt=f"Summarize this text:\n\n{request.text}",
            options=options
        ):
            # Collect text from messages
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        result_text += block.text

        # Estimate cost
        estimated_cost = 0.05 + (len(request.text) / 1000) * 0.02

        return ExecuteResponse(
            result=result_text.strip(),
            cost=round(estimated_cost, 2),
            subtask_type="summarize",
            requires_external_tool=False,
            external_cost=0.0
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "summarizer",
        "powered_by": "Claude Agent SDK (Official)",
        "framework": "claude-agent-sdk"
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Summarizer Agent",
        "description": "Text summarization using official Claude Agent SDK",
        "skills": ["summarize", "analyze", "condense"],
        "base_price": 0.05,
        "agent_type": "claude_agent_sdk",
        "framework": "claude-agent-sdk"
    }


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        exit(1)

    uvicorn.run(app, host="0.0.0.0", port=8001)
