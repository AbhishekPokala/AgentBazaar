from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import get_db
from db.repositories.task_repository import TaskRepository
from db.repositories.task_step_repository import TaskStepRepository
from models.task import Task, TaskCreate, TaskStep

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[Task])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    """Get all tasks"""
    repo = TaskRepository(db)
    return await repo.get_all()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    """Get task by ID"""
    repo = TaskRepository(db)
    task = await repo.get_by_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    
    return task


@router.get("/{task_id}/steps", response_model=List[TaskStep])
async def get_task_steps(task_id: str, db: AsyncSession = Depends(get_db)):
    """Get all steps for a task"""
    # First verify task exists
    task_repo = TaskRepository(db)
    task = await task_repo.get_by_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
    
    # Get steps
    step_repo = TaskStepRepository(db)
    return await step_repo.get_by_task_id(task_id)


@router.post("", response_model=Task, status_code=201)
async def create_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db)):
    """Create a new task"""
    repo = TaskRepository(db)
    return await repo.create(task_data)
