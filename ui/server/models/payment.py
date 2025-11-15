from pydantic import BaseModel
from datetime import datetime


class BazaarBucksPaymentBase(BaseModel):
    """Base BazaarBucks payment schema"""
    task_id: str
    agent_id: str
    amount: float
    type: str = "agent_payment"


class BazaarBucksPaymentCreate(BazaarBucksPaymentBase):
    """Schema for creating a BazaarBucks payment"""
    pass


class BazaarBucksPayment(BazaarBucksPaymentBase):
    """Schema for BazaarBucks payment response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class StripePaymentBase(BaseModel):
    """Base Stripe payment schema"""
    agent_id: str
    vendor: str
    amount: float
    status: str = "completed"
    type: str = "card_spend"


class StripePaymentCreate(StripePaymentBase):
    """Schema for creating a Stripe payment"""
    pass


class StripePayment(StripePaymentBase):
    """Schema for Stripe payment response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
