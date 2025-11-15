"""
Mock High Price Agent - Simulates expensive pricing scenarios
Simple FastAPI service (no Claude Agent SDK needed for mocks)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock High Price Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    task: str
    negotiated_price: float = None  # Optional negotiated price


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
    Execute task with high pricing.
    Will accept negotiated price if provided.
    """
    # Base high price
    base_price = 0.85

    # Use negotiated price if provided
    if request.negotiated_price is not None:
        final_price = request.negotiated_price
        result_msg = f"Task completed at negotiated price: {request.task}"
    else:
        final_price = base_price
        result_msg = f"Task completed at premium price: {request.task}"

    return ExecuteResponse(
        result=result_msg,
        cost=round(final_price, 2),
        subtask_type="premium",
        requires_external_tool=False,
        external_cost=0.0
    )


@app.get("/price")
async def get_price():
    """Return current pricing information"""
    return {
        "base_price": 0.85,
        "negotiable": True,
        "min_price": 0.50,
        "reason": "Premium quality service"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "mock_highprice",
        "pricing_tier": "premium",
        "framework": "mock"
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Premium Agent (Mock)",
        "description": "Simulates premium pricing scenarios",
        "skills": ["premium"],
        "base_price": 0.85,
        "agent_type": "mock",
        "purpose": "testing"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)

