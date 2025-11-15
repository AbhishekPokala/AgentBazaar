from sqlalchemy import Column, String, Float, Integer, Boolean, ARRAY, Text
from db.database import Base


class Agent(Base):
    """Agent SQLAlchemy model"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    skills = Column(ARRAY(Text), nullable=False)
    base_price = Column(Float, nullable=False)
    dynamic_price = Column(Float, nullable=False)
    load = Column(Integer, nullable=False, default=0)
    rating = Column(Float, nullable=False, default=5.0)
    jobs_completed = Column(Integer, nullable=False, default=0)
    endpoint_url = Column(Text, nullable=False)
    capabilities = Column(ARRAY(Text), nullable=False)
    avg_response_time = Column(Integer, nullable=False, default=1000)  # ms
    availability = Column(Boolean, nullable=False, default=True)
