"""
Agent Management API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.database import get_db
from db.repositories import AgentRepository
from models.agent import Agent, AgentCreate, AgentUpdate

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=List[Agent])
async def get_agents(db: AsyncSession = Depends(get_db)):
    """
    Get all agents
    
    Returns list of all available agents with their details:
    - Basic info (name, description)
    - Skills and capabilities
    - Performance metrics (rating, jobs completed, response time)
    - Pricing (base price, dynamic price)
    - Availability status
    """
    repo = AgentRepository(db)
    return await repo.get_all()


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    """
    Get agent by ID
    
    Returns detailed information about a specific agent.
    """
    repo = AgentRepository(db)
    agent = await repo.get_by_id(agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.post("", response_model=Agent, status_code=201)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create new agent
    
    Register a new agent in the marketplace.
    """
    repo = AgentRepository(db)
    return await repo.create(agent_data)


@router.patch("/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update agent
    
    Update agent information (pricing, availability, etc.)
    """
    repo = AgentRepository(db)
    agent = await repo.update(agent_id, agent_data)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    """
    Delete agent
    
    Remove an agent from the marketplace.
    """
    repo = AgentRepository(db)
    success = await repo.delete(agent_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return None
