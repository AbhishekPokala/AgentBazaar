from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base Task schema"""
    user_query: str
    required_skills: List[str]
    status: str = "created"
    max_budget: float = 1.0
    total_cost: float = 0.0


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class Task(TaskBase):
    """Schema for task response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskStepBase(BaseModel):
    """Base TaskStep schema"""
    task_id: str
    agent_id: str
    subtask_type: str
    status: str = "pending"
    cost: float = 0.0
    external_cost: float = 0.0
    requires_external_tool: bool = False
    result: Optional[str] = None
    execution_time: Optional[int] = None  # ms


class TaskStepCreate(TaskStepBase):
    """Schema for creating a task step"""
    pass


class TaskStep(TaskStepBase):
    """Schema for task step response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
