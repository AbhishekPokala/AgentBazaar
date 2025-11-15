from pydantic import BaseModel
from typing import List, Optional


class AgentBase(BaseModel):
    """Base Agent schema"""
    name: str
    description: str
    skills: List[str]
    base_price: float
    dynamic_price: float
    load: float = 0.0
    rating: float = 5.0
    jobs_completed: int = 0
    endpoint_url: str
    capabilities: List[str]
    avg_response_time: float = 1000.0  # ms
    availability: bool = True


class AgentCreate(AgentBase):
    """Schema for creating an agent"""
    id: str


class AgentUpdate(BaseModel):
    """Schema for updating an agent (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    base_price: Optional[float] = None
    dynamic_price: Optional[float] = None
    load: Optional[float] = None
    rating: Optional[float] = None
    jobs_completed: Optional[int] = None
    endpoint_url: Optional[str] = None
    capabilities: Optional[List[str]] = None
    avg_response_time: Optional[float] = None
    availability: Optional[bool] = None


class Agent(AgentBase):
    """Schema for agent response (matches UI TypeScript schema)"""
    id: str
    
    class Config:
        from_attributes = True
