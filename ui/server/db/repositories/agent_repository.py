"""
Agent repository for database operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from db.models.agent import Agent as AgentModel
from models.agent import Agent, AgentCreate, AgentUpdate


class AgentRepository:
    """Repository for Agent CRUD operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Agent]:
        """Get all agents"""
        result = await self.session.execute(select(AgentModel))
        agents = result.scalars().all()
        return [Agent.model_validate(agent) for agent in agents]
    
    async def get_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        result = await self.session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        return Agent.model_validate(agent) if agent else None
    
    async def create(self, agent_data: AgentCreate) -> Agent:
        """Create new agent"""
        # Check if agent with same ID already exists
        existing = await self.get_by_id(agent_data.id)
        if existing:
            from fastapi import HTTPException
            raise HTTPException(status_code=409, detail=f"Agent with ID '{agent_data.id}' already exists")
        
        # Validate dynamic_price >= base_price
        if agent_data.dynamic_price < agent_data.base_price:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"dynamic_price ({agent_data.dynamic_price}) must be >= base_price ({agent_data.base_price})"
            )
        
        agent = AgentModel(**agent_data.model_dump())
        self.session.add(agent)
        await self.session.commit()
        await self.session.refresh(agent)
        return Agent.model_validate(agent)
    
    async def update(self, agent_id: str, agent_data: AgentUpdate) -> Optional[Agent]:
        """Update agent"""
        result = await self.session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            return None
        
        # Update only provided fields
        update_data = agent_data.model_dump(exclude_unset=True)
        
        # Validate dynamic_price >= base_price after update
        new_base = update_data.get("base_price", agent.base_price)
        new_dynamic = update_data.get("dynamic_price", agent.dynamic_price)
        if new_dynamic < new_base:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"dynamic_price ({new_dynamic}) must be >= base_price ({new_base})"
            )
        
        for key, value in update_data.items():
            setattr(agent, key, value)
        
        await self.session.commit()
        await self.session.refresh(agent)
        return Agent.model_validate(agent)
    
    async def delete(self, agent_id: str) -> bool:
        """Delete agent"""
        result = await self.session.execute(
            select(AgentModel).where(AgentModel.id == agent_id)
        )
        agent = result.scalar_one_or_none()
        
        if not agent:
            return False
        
        await self.session.delete(agent)
        await self.session.commit()
        return True
