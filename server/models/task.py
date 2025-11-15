from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base Task schema"""
    model_config = ConfigDict(populate_by_name=True)
    
    user_query: str = Field(alias="userQuery", serialization_alias="userQuery")
    required_skills: List[str] = Field(alias="requiredSkills", serialization_alias="requiredSkills")
    status: str = "created"
    max_budget: float = Field(default=1.0, alias="maxBudget", serialization_alias="maxBudget")
    total_cost: float = Field(default=0.0, alias="totalCost", serialization_alias="totalCost")


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    model_config = ConfigDict(populate_by_name=True)


class Task(TaskBase):
    """Schema for task response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    completed_at: Optional[datetime] = Field(None, alias="completedAt", serialization_alias="completedAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TaskStepBase(BaseModel):
    """Base TaskStep schema"""
    model_config = ConfigDict(populate_by_name=True)
    
    task_id: str = Field(alias="taskId", serialization_alias="taskId")
    agent_id: str = Field(alias="agentId", serialization_alias="agentId")
    subtask_type: str = Field(alias="subtaskType", serialization_alias="subtaskType")
    status: str = "pending"
    cost: float = 0.0
    external_cost: float = Field(default=0.0, alias="externalCost", serialization_alias="externalCost")
    requires_external_tool: bool = Field(default=False, alias="requiresExternalTool", serialization_alias="requiresExternalTool")
    result: Optional[str] = None
    execution_time: Optional[int] = Field(None, alias="executionTime", serialization_alias="executionTime")


class TaskStepCreate(TaskStepBase):
    """Schema for creating a task step"""
    model_config = ConfigDict(populate_by_name=True)


class TaskStep(TaskStepBase):
    """Schema for task step response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    completed_at: Optional[datetime] = Field(None, alias="completedAt", serialization_alias="completedAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
