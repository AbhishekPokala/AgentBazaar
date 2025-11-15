"""
Translator Agent - Uses Official Claude Agent SDK
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn
from claude_agent_sdk import query, ClaudeAgentOptions

app = FastAPI(title="Translator Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    text: str
    target_language: str = "es"
    source_language: str = "auto"


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
    Execute language translation using Claude Agent SDK.
    """
    try:
        # Build prompt
        if request.source_language == "auto":
            prompt = f"Translate the following text to {request.target_language}. Provide only the translation:\n\n{request.text}"
        else:
            prompt = f"Translate from {request.source_language} to {request.target_language}. Provide only the translation:\n\n{request.text}"

        # Configure agent with Claude Agent SDK
        options = ClaudeAgentOptions(
            system_prompt="""You are a professional translation agent.

Guidelines:
- Translate accurately while preserving meaning and tone
- Adapt idioms and cultural references appropriately
- Maintain formatting and structure
- Provide natural, fluent translations
- Only return the translation, no explanations""",
            allowed_tools=[],  # No tools needed
            permission_mode="bypassPermissions"
        )

        # Use Claude Agent SDK query() function
        result_text = ""
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        result_text += block.text

        # Estimate cost
        estimated_cost = 0.10 + (len(request.text) / 1000) * 0.05

        return ExecuteResponse(
            result=result_text.strip(),
            cost=round(estimated_cost, 2),
            subtask_type="translate",
            requires_external_tool=False,
            external_cost=0.0
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "translator",
        "powered_by": "Claude Agent SDK (Official)",
        "framework": "claude-agent-sdk"
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Translator Agent",
        "description": "Language translation using official Claude Agent SDK",
        "skills": ["translate", "language_detection", "localization"],
        "base_price": 0.10,
        "agent_type": "claude_agent_sdk",
        "framework": "claude-agent-sdk"
    }


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        exit(1)

    uvicorn.run(app, host="0.0.0.0", port=8002)
