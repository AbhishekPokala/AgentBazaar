"""
HubChat API Routes
Conversational interface with context retention
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from db.database import get_db
from db.repositories.message_repository import MessageRepository
from db.repositories.task_repository import TaskRepository
from models.message import Message, MessageCreate
from hubchat.conversational_orchestrator import ConversationalOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/hubchat", tags=["hubchat"])


class ChatMessageRequest(BaseModel):
    """Request to send a chat message"""
    content: str
    task_id: Optional[str] = None
    max_budget: Optional[float] = None


class ChatMessageResponse(BaseModel):
    """Response from chat message"""
    success: bool
    user_message: Message
    assistant_message: Message
    cost_breakdown: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None


# Initialize orchestrator (singleton)
orchestrator: Optional[ConversationalOrchestrator] = None


def get_orchestrator() -> ConversationalOrchestrator:
    """Get or create the orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        try:
            orchestrator = ConversationalOrchestrator()
            logger.info("Orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize orchestrator. Make sure ANTHROPIC_API_KEY is set: {str(e)}"
            )
    return orchestrator


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    request: ChatMessageRequest,
    session: AsyncSession = Depends(get_db)
):
    """
    Send a message to HubChat orchestrator.
    Maintains full conversation context for continuous dialogue.
    
    The orchestrator can:
    - Answer questions
    - Ask for clarifications
    - Create tasks
    - Invoke agents
    - Track costs
    """
    try:
        # Get repositories
        message_repo = MessageRepository(session)
        task_repo = TaskRepository(session)
        
        # Get conversation history
        if request.task_id:
            # Get messages for this specific task
            history = await message_repo.get_by_task_id(request.task_id)
            
            # Verify task exists
            task = await task_repo.get_by_id(request.task_id)
            if not task:
                raise HTTPException(
                    status_code=404,
                    detail=f"Task {request.task_id} not found"
                )
        else:
            # Get all messages (general conversation)
            history = await message_repo.get_all(limit=100)
        
        # Convert to conversation format
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        logger.info(f"Processing message with {len(conversation_history)} previous messages")
        
        # Store user message
        user_message_data = MessageCreate(
            role="user",
            content=request.content,
            task_id=request.task_id
        )
        user_message = await message_repo.create(user_message_data)
        
        # Get orchestrator and process message
        orch = get_orchestrator()
        result = await orch.process_message(
            user_message=request.content,
            conversation_history=conversation_history,
            task_id=request.task_id,
            max_budget=request.max_budget
        )
        
        # Store assistant response
        assistant_message_data = MessageCreate(
            role="assistant",
            content=result["response"],
            task_id=result.get("task_id", request.task_id),
            cost_breakdown=result.get("cost_breakdown")
        )
        assistant_message = await message_repo.create(assistant_message_data)
        
        return ChatMessageResponse(
            success=result["success"],
            user_message=user_message,
            assistant_message=assistant_message,
            cost_breakdown=result.get("cost_breakdown"),
            task_id=result.get("task_id", request.task_id)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )


@router.get("/messages", response_model=List[Message])
async def get_messages(
    task_id: Optional[str] = None,
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    """
    Get chat message history.
    
    If task_id is provided, returns messages for that task only.
    Otherwise returns all messages (general conversation).
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
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching messages: {str(e)}"
        )


@router.delete("/messages/{task_id}")
async def delete_task_messages(
    task_id: str,
    session: AsyncSession = Depends(get_db)
):
    """
    Delete all messages for a specific task.
    Useful for clearing conversation history.
    """
    try:
        message_repo = MessageRepository(session)
        count = await message_repo.delete_by_task_id(task_id)
        
        return {
            "success": True,
            "deleted_count": count,
            "message": f"Deleted {count} messages for task {task_id}"
        }
        
    except Exception as e:
        logger.error(f"Error deleting messages: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting messages: {str(e)}"
        )
