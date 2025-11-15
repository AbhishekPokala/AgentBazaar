from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from db.models.task import TaskStep as TaskStepModel
from models.task import TaskStep, TaskStepCreate
import uuid


class TaskStepRepository:
    """Repository for TaskStep CRUD operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_task_id(self, task_id: str) -> List[TaskStep]:
        """Get all steps for a task"""
        result = await self.session.execute(
            select(TaskStepModel)
            .where(TaskStepModel.task_id == task_id)
            .order_by(TaskStepModel.created_at.asc())
        )
        steps = result.scalars().all()
        return [TaskStep.model_validate(step) for step in steps]
    
    async def get_by_id(self, step_id: str) -> Optional[TaskStep]:
        """Get task step by ID"""
        result = await self.session.execute(
            select(TaskStepModel).where(TaskStepModel.id == step_id)
        )
        step = result.scalar_one_or_none()
        return TaskStep.model_validate(step) if step else None
    
    async def create(self, step_data: TaskStepCreate) -> TaskStep:
        """Create new task step"""
        # Validate cost
        if step_data.cost < 0:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"cost must be non-negative, got {step_data.cost}"
            )
        
        # Generate unique ID
        step_id = str(uuid.uuid4())
        
        step = TaskStepModel(
            id=step_id,
            **step_data.model_dump(by_alias=False)
        )
        self.session.add(step)
        await self.session.commit()
        await self.session.refresh(step)
        return TaskStep.model_validate(step)
    
    async def update_status(
        self,
        step_id: str,
        status: str,
        result: Optional[str] = None,
        execution_time: Optional[int] = None,
        external_cost: Optional[float] = None,
        completed_at: Optional[datetime] = None
    ) -> Optional[TaskStep]:
        """Update task step status, result, and costs"""
        from datetime import datetime
        
        db_result = await self.session.execute(
            select(TaskStepModel).where(TaskStepModel.id == step_id)
        )
        step = db_result.scalar_one_or_none()
        
        if not step:
            return None
        
        step.status = status
        if result is not None:
            step.result = result
        if execution_time is not None:
            step.execution_time = execution_time
        if external_cost is not None:
            step.external_cost = external_cost
        if completed_at is not None:
            step.completed_at = completed_at
        
        await self.session.commit()
        await self.session.refresh(step)
        return TaskStep.model_validate(step)
    
    async def delete(self, step_id: str) -> bool:
        """Delete task step"""
        result = await self.session.execute(
            select(TaskStepModel).where(TaskStepModel.id == step_id)
        )
        step = result.scalar_one_or_none()
        
        if not step:
            return False
        
        await self.session.delete(step)
        await self.session.commit()
        return True
