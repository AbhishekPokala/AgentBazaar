from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    """Base Message schema"""
    model_config = ConfigDict(populate_by_name=True)
    
    role: str  # user, assistant
    content: str
    task_id: Optional[str] = Field(None, alias="taskId", serialization_alias="taskId")
    cost_breakdown: Optional[Dict[str, Any]] = Field(None, alias="costBreakdown", serialization_alias="costBreakdown")


class MessageCreate(MessageBase):
    """Schema for creating a message"""
    model_config = ConfigDict(populate_by_name=True)


class Message(MessageBase):
    """Schema for message response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
