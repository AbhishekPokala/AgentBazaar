from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class AgentBase(BaseModel):
    """Base Agent schema"""
    model_config = ConfigDict(populate_by_name=True)
    
    name: str
    description: str
    skills: List[str]
    base_price: float = Field(alias="basePrice", serialization_alias="basePrice")
    dynamic_price: float = Field(alias="dynamicPrice", serialization_alias="dynamicPrice")
    load: float = 0.0
    rating: float = 5.0
    jobs_completed: int = Field(default=0, alias="jobsCompleted", serialization_alias="jobsCompleted")
    endpoint_url: str = Field(alias="endpointUrl", serialization_alias="endpointUrl")
    capabilities: List[str]
    avg_response_time: float = Field(default=1000.0, alias="avgResponseTime", serialization_alias="avgResponseTime")
    availability: bool = True


class AgentCreate(AgentBase):
    """Schema for creating an agent"""
    id: str
    model_config = ConfigDict(populate_by_name=True)


class AgentUpdate(BaseModel):
    """Schema for updating an agent (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    base_price: Optional[float] = Field(None, alias="basePrice", serialization_alias="basePrice")
    dynamic_price: Optional[float] = Field(None, alias="dynamicPrice", serialization_alias="dynamicPrice")
    load: Optional[float] = None
    rating: Optional[float] = None
    jobs_completed: Optional[int] = Field(None, alias="jobsCompleted", serialization_alias="jobsCompleted")
    endpoint_url: Optional[str] = Field(None, alias="endpointUrl", serialization_alias="endpointUrl")
    capabilities: Optional[List[str]] = None
    avg_response_time: Optional[float] = Field(None, alias="avgResponseTime", serialization_alias="avgResponseTime")
    availability: Optional[bool] = None
    
    model_config = ConfigDict(populate_by_name=True)


class Agent(AgentBase):
    """Schema for agent response (matches UI TypeScript schema)"""
    id: str
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
