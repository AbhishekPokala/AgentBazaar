"""
FastAPI wrapper for HubChat Orchestrator
Exposes HubChat via HTTP API for ChatGPT Actions
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import os
import logging

from orchestrator import process_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="HubChat Orchestrator API",
    description="Central orchestrator for Agent Marketplace. Coordinates multiple AI agents to complete complex tasks.",
    version="1.0.0",
    servers=[
        {"url": os.getenv("PUBLIC_URL", "http://localhost:8000"), "description": "HubChat API Server"}
    ]
)

# Enable CORS for ChatGPT to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://chatgpt.com", "*"],  # ChatGPT domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Request to process a user query"""
    query: str = Field(..., description="Natural language query describing the task")
    max_budget: Optional[float] = Field(None, description="Optional maximum budget in USD")

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Summarize this article and translate to French: [article text]",
                "max_budget": 1.0
            }
        }


class QueryResponse(BaseModel):
    """Response from HubChat"""
    success: bool
    output: str
    cost_breakdown: dict
    agents_used: list


@app.post("/query", response_model=QueryResponse)
async def query_hubchat(request: QueryRequest) -> QueryResponse:
    """
    Process a user query through HubChat orchestrator.

    HubChat will:
    1. Understand the request
    2. Plan which agents to use
    3. Coordinate multiple agents if needed
    4. Return aggregated results with cost breakdown

    Example queries:
    - "Translate 'Hello World' to Spanish"
    - "Summarize this text: [long text]"
    - "Search for Claude AI and summarize the results"
    - "Translate this text to French and then summarize it"
    """
    logger.info(f"Received query: {request.query[:100]}...")

    try:
        result = await process_request(
            user_query=request.query,
            max_budget=request.max_budget
        )

        logger.info(f"Query processed successfully. Agents used: {len(result.get('agents_used', []))}")
        return QueryResponse(**result)

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "HubChat Orchestrator",
        "agents_available": ["summarizer", "translator", "search", "mock_busy", "mock_highprice", "mock_negotiator"]
    }


@app.get("/agents")
async def list_agents():
    """List available agents and their capabilities"""
    return {
        "agents": [
            {
                "id": "summarizer",
                "name": "Summarizer Agent",
                "description": "Text summarization using Claude",
                "skills": ["summarize", "condense", "analyze"],
                "base_price": 0.05,
                "endpoint": "http://localhost:8001"
            },
            {
                "id": "translator",
                "name": "Translator Agent",
                "description": "Language translation using Claude",
                "skills": ["translate"],
                "base_price": 0.10,
                "endpoint": "http://localhost:8002"
            },
            {
                "id": "search",
                "name": "Search Agent",
                "description": "Web search with synthesis",
                "skills": ["search", "research"],
                "base_price": 0.08,
                "endpoint": "http://localhost:8003"
            }
        ]
    }


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "service": "HubChat Orchestrator API",
        "description": "Multi-agent coordination for complex AI tasks",
        "version": "1.0.0",
        "endpoints": {
            "POST /query": "Submit a query to HubChat",
            "GET /agents": "List available agents",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation",
            "GET /openapi.json": "OpenAPI spec for ChatGPT Actions"
        },
        "example_usage": {
            "endpoint": "/query",
            "method": "POST",
            "body": {
                "query": "Translate 'Hello World' to Spanish",
                "max_budget": 0.5
            }
        }
    }


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        exit(1)

    print("=" * 60)
    print("🚀 Starting HubChat Orchestrator API")
    print("=" * 60)
    print(f"📍 API: http://localhost:8000")
    print(f"📖 Docs: http://localhost:8000/docs")
    print(f"🔧 OpenAPI: http://localhost:8000/openapi.json")
    print("=" * 60)
    print("\n⚠️  Make sure agents are running first!")
    print("   Run: ./start_all_services.sh\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

