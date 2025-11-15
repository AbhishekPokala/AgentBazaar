"""
Mock Negotiation Agent - Simulates price negotiation
Simple FastAPI service (no Claude Agent SDK needed for mocks)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Mock Negotiation Agent", version="1.0.0")


class ExecuteRequest(BaseModel):
    """Uniform request format"""
    task: str
    offered_price: float = None  # Price offered by buyer


class ExecuteResponse(BaseModel):
    """Uniform response format"""
    result: str
    cost: float
    subtask_type: str
    requires_external_tool: bool
    external_cost: float


class NegotiationRequest(BaseModel):
    """Negotiation-specific request"""
    offered_price: float
    round: int = 1


class NegotiationResponse(BaseModel):
    """Negotiation response"""
    accepted: bool
    counter_offer: float = None
    message: str


@app.post("/execute", response_model=ExecuteResponse)
async def execute(request: ExecuteRequest) -> ExecuteResponse:
    """
    Execute task after price negotiation.
    """
    initial_price = 0.60
    min_acceptable_price = 0.40

    # If no offered price, return at initial price
    if request.offered_price is None:
        final_price = initial_price
        result_msg = f"Task completed at standard price: {request.task}"
    else:
        # Check if offered price is acceptable
        if request.offered_price >= min_acceptable_price:
            final_price = request.offered_price
            result_msg = f"Task completed at agreed price ${final_price:.2f}: {request.task}"
        else:
            raise HTTPException(
                status_code=402,
                detail=f"Offered price ${request.offered_price:.2f} is too low. Minimum is ${min_acceptable_price:.2f}"
            )

    return ExecuteResponse(
        result=result_msg,
        cost=round(final_price, 2),
        subtask_type="negotiable",
        requires_external_tool=False,
        external_cost=0.0
    )


@app.post("/negotiate", response_model=NegotiationResponse)
async def negotiate(request: NegotiationRequest) -> NegotiationResponse:
    """
    Handle price negotiation.
    """
    initial_price = 0.60
    min_acceptable_price = 0.40

    offered = request.offered_price
    round_num = request.round

    # Negotiation logic
    if offered >= initial_price * 0.85:  # Within 15% of asking
        return NegotiationResponse(
            accepted=True,
            message=f"Great! I accept ${offered:.2f}. Let's proceed."
        )
    elif offered >= min_acceptable_price:
        # Counter offer - meet in the middle
        counter = (offered + initial_price) / 2
        counter = round(counter, 2)

        if round_num >= 3:  # After 3 rounds, accept if above minimum
            return NegotiationResponse(
                accepted=True,
                message=f"Okay, I'll accept ${offered:.2f} since we've been negotiating."
            )

        return NegotiationResponse(
            accepted=False,
            counter_offer=counter,
            message=f"I appreciate your offer of ${offered:.2f}, but can we meet at ${counter:.2f}?"
        )
    else:
        return NegotiationResponse(
            accepted=False,
            counter_offer=min_acceptable_price,
            message=f"I'm sorry, but ${offered:.2f} is too low. My minimum is ${min_acceptable_price:.2f}."
        )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "mock_negotiator",
        "negotiable": True,
        "framework": "mock"
    }


@app.get("/info")
async def info():
    """Agent information"""
    return {
        "name": "Negotiator Agent (Mock)",
        "description": "Simulates price negotiation scenarios",
        "skills": ["negotiable"],
        "base_price": 0.60,
        "agent_type": "mock",
        "purpose": "testing"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)

