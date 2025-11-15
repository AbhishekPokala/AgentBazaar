from sqlalchemy import Column, String, Text, Float, DateTime, ARRAY, Integer, Boolean
from sqlalchemy.sql import func
from db.database import Base


class Task(Base):
    """Task SQLAlchemy model"""
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True)
    user_query = Column(Text, nullable=False)
    required_skills = Column(ARRAY(Text), nullable=False)
    status = Column(Text, nullable=False, default="created")  # created, in_progress, completed, failed
    max_budget = Column(Float, nullable=False, default=1.0)
    total_cost = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class TaskStep(Base):
    """TaskStep SQLAlchemy model - execution timeline"""
    __tablename__ = "task_steps"
    
    id = Column(String, primary_key=True)
    task_id = Column(String, nullable=False)
    agent_id = Column(String, nullable=False)
    subtask_type = Column(Text, nullable=False)
    status = Column(Text, nullable=False, default="pending")  # pending, in_progress, completed, failed
    cost = Column(Float, nullable=False, default=0.0)
    external_cost = Column(Float, nullable=False, default=0.0)
    requires_external_tool = Column(Boolean, nullable=False, default=False)
    result = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # ms
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
