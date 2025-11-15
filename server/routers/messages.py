"""
Messages API Routes
Provides /api/messages endpoint for frontend
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from db.database import get_db
from db.repositories.message_repository import MessageRepository
from models.message import Message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["messages"])


@router.get("/messages", response_model=List[Message])
async def get_messages(
    task_id: str | None = None,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    """
    Get all chat messages or messages for a specific task.
    """
    try:
        message_repo = MessageRepository(session)
        
        if task_id:
            messages = await message_repo.get_by_task_id(task_id)
        else:
            messages = await message_repo.get_all(limit=limit)
        
        return messages
        
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}", exc_info=True)
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching messages: {str(e)}"
        )
