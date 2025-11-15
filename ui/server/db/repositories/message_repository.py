from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from db.models.message import Message as MessageModel
from models.message import Message, MessageCreate
import uuid


class MessageRepository:
    """Repository for Message CRUD operations"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all(self, limit: int = 100) -> List[Message]:
        """Get all messages ordered by creation time"""
        result = await self.session.execute(
            select(MessageModel)
            .order_by(MessageModel.created_at.asc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return [Message.model_validate(msg) for msg in messages]
    
    async def get_by_id(self, message_id: str) -> Optional[Message]:
        """Get a single message by ID"""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        message = result.scalar_one_or_none()
        return Message.model_validate(message) if message else None
    
    async def get_by_task_id(self, task_id: str) -> List[Message]:
        """Get all messages for a specific task"""
        result = await self.session.execute(
            select(MessageModel)
            .where(MessageModel.task_id == task_id)
            .order_by(MessageModel.created_at.asc())
        )
        messages = result.scalars().all()
        return [Message.model_validate(msg) for msg in messages]
    
    async def create(self, message_data: MessageCreate) -> Message:
        """Create a new message"""
        # Generate unique ID
        message_id = str(uuid.uuid4())
        
        message = MessageModel(
            id=message_id,
            **message_data.model_dump()
        )
        
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return Message.model_validate(message)
    
    async def delete(self, message_id: str) -> bool:
        """Delete a message"""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            return False
        
        await self.session.delete(message)
        await self.session.commit()
        return True
    
    async def delete_by_task_id(self, task_id: str) -> int:
        """Delete all messages for a task. Returns number of deleted messages."""
        result = await self.session.execute(
            select(MessageModel).where(MessageModel.task_id == task_id)
        )
        messages = result.scalars().all()
        
        count = len(messages)
        for message in messages:
            await self.session.delete(message)
        
        await self.session.commit()
        return count
