from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from db.models.task import Task as TaskModel
from models.task import Task, TaskCreate
import uuid


class TaskRepository:
    """Repository for Task CRUD operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self) -> List[Task]:
        """Get all tasks"""
        result = await self.session.execute(
            select(TaskModel).order_by(TaskModel.created_at.desc())
        )
        tasks = result.scalars().all()
        return [Task.model_validate(task) for task in tasks]
    
    async def get_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        return Task.model_validate(task) if task else None
    
    async def create(self, task_data: TaskCreate) -> Task:
        """Create new task"""
        # Validate budget
        if task_data.max_budget <= 0:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"max_budget must be positive, got {task_data.max_budget}"
            )
        
        # Generate unique ID
        task_id = str(uuid.uuid4())
        
        task = TaskModel(
            id=task_id,
            **task_data.model_dump()
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return Task.model_validate(task)
    
    async def update_status(
        self, 
        task_id: str, 
        status: str,
        total_cost: Optional[float] = None,
        completed_at: Optional[datetime] = None
    ) -> Optional[Task]:
        """Update task status and optionally total_cost and completed_at"""
        from datetime import datetime
        
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            return None
        
        task.status = status
        if total_cost is not None:
            task.total_cost = total_cost
        if completed_at is not None:
            task.completed_at = completed_at
        
        await self.session.commit()
        await self.session.refresh(task)
        return Task.model_validate(task)
    
    async def delete(self, task_id: str) -> bool:
        """Delete task"""
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        
        if not task:
            return False
        
        await self.session.delete(task)
        await self.session.commit()
        return True
