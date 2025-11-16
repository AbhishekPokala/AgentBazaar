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
# server/routers/hubchat.py is 1 level deep from server root
server_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, server_dir)

from db.database import get_db
from db.repositories.message_repository import MessageRepository
from db.repositories.task_repository import TaskRepository
from models.message import Message, MessageCreate

# Import Orchestrator from server/hubchat
from hubchat.orchestrator import HubChatOrchestrator

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
    orchestration_data: Optional[Dict[str, Any]] = None
    cost_breakdown: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None


# Initialize orchestrator (singleton)
orchestrator: Optional[HubChatOrchestrator] = None


def get_orchestrator() -> HubChatOrchestrator:
    """Get or create the orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        try:
            orchestrator = HubChatOrchestrator()
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
    Single-turn orchestration: discovers agents, invokes them, processes payments.
    
    The orchestrator:
    - Discovers agents matching user query
    - Invokes selected agents
    - Processes USDC payments via Locus blockchain
    - Returns orchestration metadata
    """
    try:
        # Get repositories
        message_repo = MessageRepository(session)
        
        logger.info(f"Processing query: {request.content[:100]}...")
        
        # Store user message
        user_message_data = MessageCreate(
            role="user",
            content=request.content,
            task_id=request.task_id
        )
        user_message = await message_repo.create(user_message_data)
        
        # Get orchestrator and process request (synchronous call)
        orch = get_orchestrator()
        result = orch.process_user_request(
            user_query=request.content,
            max_budget=request.max_budget or 10.0
        )
        
        # Extract orchestration data
        orchestration_data = {
            "agents_discovered": result.get("agents_discovered", []),
            "agents_used": result.get("agents_used", []),
            "payments_made": result.get("payments_made", []),
            "total_paid": result.get("total_paid", 0.0)
        }
        
        # Store assistant response
        assistant_message_data = MessageCreate(
            role="assistant",
            content=result["output"],
            task_id=request.task_id,
            orchestration_data=orchestration_data
        )
        assistant_message = await message_repo.create(assistant_message_data)
        
        logger.info(f"Orchestration complete: {len(orchestration_data['agents_discovered'])} discovered, "
                   f"{len(orchestration_data['agents_used'])} used, ${orchestration_data['total_paid']:.2f} paid")
        
        return ChatMessageResponse(
            success=True,
            user_message=user_message,
            assistant_message=assistant_message,
            orchestration_data=orchestration_data,
            task_id=request.task_id
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
