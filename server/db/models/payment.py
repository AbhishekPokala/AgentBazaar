from sqlalchemy import Column, String, Float, Text, DateTime
from sqlalchemy.sql import func
from db.database import Base


class BazaarBucksPayment(Base):
    """BazaarBucks internal payment model"""
    __tablename__ = "bazaarbucks_payments"
    
    id = Column(String, primary_key=True)
    task_id = Column(String, nullable=False)
    agent_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Text, nullable=False, default="agent_payment")  # agent_payment, platform_fee, refund
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class StripePayment(Base):
    """Stripe external payment model"""
    __tablename__ = "stripe_payments"
    
    id = Column(String, primary_key=True)
    agent_id = Column(String, nullable=False)
    vendor = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Text, nullable=False, default="completed")  # pending, completed, failed
    type = Column(Text, nullable=False, default="card_spend")  # card_spend, balance_load
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
