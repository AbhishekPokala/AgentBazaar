from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from db.database import Base


class Message(Base):
    """HubChat message model"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    role = Column(Text, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    task_id = Column(String, nullable=True)
    cost_breakdown = Column(JSON, nullable=True)  # {"subtasks": [...], "total": 0.0}
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
