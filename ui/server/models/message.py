from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    """Base Message schema"""
    role: str  # user, assistant
    content: str
    task_id: Optional[str] = None
    cost_breakdown: Optional[Dict[str, Any]] = None


class MessageCreate(MessageBase):
    """Schema for creating a message"""
    pass


class Message(MessageBase):
    """Schema for message response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
