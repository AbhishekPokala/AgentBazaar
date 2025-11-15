from pydantic import BaseModel
from typing import List


class AgentBase(BaseModel):
    """Base Agent schema"""
    name: str
    description: str
    skills: List[str]
    base_price: float
    dynamic_price: float
    load: int = 0
    rating: float = 5.0
    jobs_completed: int = 0
    endpoint_url: str
    capabilities: List[str]
    avg_response_time: int = 1000  # ms
    availability: bool = True


class AgentCreate(AgentBase):
    """Schema for creating an agent"""
    id: str


class Agent(AgentBase):
    """Schema for agent response (matches UI TypeScript schema)"""
    id: str
    
    class Config:
        from_attributes = True
