from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List
import httpx
from datetime import datetime
from db.database import get_db
from db.repositories.agent_repository import AgentRepository
from db.repositories.task_repository import TaskRepository
from db.repositories.task_step_repository import TaskStepRepository
from models.task import TaskStepCreate

router = APIRouter(prefix="/api", tags=["invocation"])


class AgentInvocationRequest(BaseModel):
    """Request schema for invoking an agent"""
    agent_id: str
    task_id: str
    subtask_type: str
    input_data: dict


class AgentInvocationResponse(BaseModel):
    """Response schema from agent invocation"""
    success: bool
    task_id: str
    agent_id: str
    step_id: str
    result: Optional[str] = None
    cost: float
    execution_time: int
    error: Optional[str] = None


@router.post("/invoke-agent", response_model=AgentInvocationResponse)
async def invoke_agent(
    request: AgentInvocationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Invoke an agent to execute a subtask.
    
    This endpoint:
    1. Validates the agent exists and is available
    2. Creates a task step record
    3. Calls the agent's endpoint
    4. Updates the task step with results
    5. Returns the execution result
    """
    agent_repo = AgentRepository(db)
    task_repo = TaskRepository(db)
    step_repo = TaskStepRepository(db)
    
    # Validate agent exists
    agent = await agent_repo.get_by_id(request.agent_id)
    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{request.agent_id}' not found"
        )
    
    # Validate task exists
    task = await task_repo.get_by_id(request.task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task '{request.task_id}' not found"
        )
    
    # Check if agent is available
    if not agent.availability:
        raise HTTPException(
            status_code=503,
            detail=f"Agent '{agent.name}' is currently unavailable"
        )
    
    # Create task step
    step_data = TaskStepCreate(
        task_id=request.task_id,
        agent_id=request.agent_id,
        subtask_type=request.subtask_type,
        status="in_progress",
        cost=agent.dynamic_price,
        external_cost=0.0,
        requires_external_tool=False
    )
    
    step = await step_repo.create(step_data)
    
    # Invoke the agent
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Call agent's endpoint
            response = await client.post(
                f"{agent.endpoint_url}/execute",
                json={
                    "task_id": request.task_id,
                    "subtask_type": request.subtask_type,
                    **request.input_data
                }
            )
            response.raise_for_status()
            result_data = response.json()
        
        # Calculate execution time
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Extract result and cost
        result = result_data.get("result", "")
        external_cost = result_data.get("external_cost", 0.0)
        total_cost = agent.dynamic_price + external_cost
        
        # Update step as completed with external_cost
        await step_repo.update_status(
            step_id=step.id,
            status="completed",
            result=result,
            execution_time=execution_time,
            external_cost=external_cost,
            completed_at=datetime.now()
        )
        
        # Update task total cost (handle None value)
        current_total = task.total_cost if task.total_cost is not None else 0.0
        new_total_cost = current_total + total_cost
        
        # Only update status if task isn't already completed
        new_status = task.status if task.status == "completed" else "in_progress"
        
        await task_repo.update_status(
            task_id=request.task_id,
            status=new_status,
            total_cost=new_total_cost
        )
        
        return AgentInvocationResponse(
            success=True,
            task_id=request.task_id,
            agent_id=request.agent_id,
            step_id=step.id,
            result=result,
            cost=total_cost,
            execution_time=execution_time
        )
        
    except httpx.HTTPError as e:
        # Update step as failed
        await step_repo.update_status(
            step_id=step.id,
            status="failed",
            result=f"HTTP Error: {str(e)}",
            completed_at=datetime.now()
        )
        
        # Update task status to failed if it was just created
        if task.status == "created":
            await task_repo.update_status(
                task_id=request.task_id,
                status="failed"
            )
        
        return AgentInvocationResponse(
            success=False,
            task_id=request.task_id,
            agent_id=request.agent_id,
            step_id=step.id,
            cost=0.0,
            execution_time=0,
            error=f"Failed to invoke agent: {str(e)}"
        )
    
    except Exception as e:
        # Update step as failed
        await step_repo.update_status(
            step_id=step.id,
            status="failed",
            result=f"Error: {str(e)}",
            completed_at=datetime.now()
        )
        
        # Update task status to failed if it was just created
        if task.status == "created":
            await task_repo.update_status(
                task_id=request.task_id,
                status="failed"
            )
        
        return AgentInvocationResponse(
            success=False,
            task_id=request.task_id,
            agent_id=request.agent_id,
            step_id=step.id,
            cost=0.0,
            execution_time=0,
            error=f"Unexpected error: {str(e)}"
        )
