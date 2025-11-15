"""
Mock Busy Agent - Simulates high load/busy state
Simple FastAPI service (no Claude Agent SDK needed for mocks)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import random
import time

app = FastAPI(title="Mock Busy Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    task: str


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
    Simulate a busy agent that may reject or delay requests.
    """
    # Randomly decide if agent is too busy (60% chance)
    if random.random() < 0.6:
        raise HTTPException(
            status_code=503,
            detail="Agent is currently busy. High load. Try again later or use alternative agent."
        )

    # Simulate processing delay
    time.sleep(random.uniform(1.0, 3.0))

    return ExecuteResponse(
        result=f"Task completed after delay: {request.task}",
        cost=0.12,
        subtask_type="general",
        requires_external_tool=False,
        external_cost=0.0
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    current_load = random.randint(70, 100)
    return {
        "status": "degraded" if current_load > 80 else "healthy",
        "agent": "mock_busy",
        "load": current_load,
        "framework": "mock"
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Busy Agent (Mock)",
        "description": "Simulates high load scenarios for testing",
        "skills": ["general"],
        "base_price": 0.12,
        "agent_type": "mock",
        "purpose": "testing"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)

