from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BazaarBucksPaymentBase(BaseModel):
    """Base BazaarBucks payment schema"""
    task_id: str = Field(alias="taskId", serialization_alias="taskId")
    agent_id: str = Field(alias="agentId", serialization_alias="agentId")
    amount: float
    type: str = "agent_payment"


class BazaarBucksPaymentCreate(BazaarBucksPaymentBase):
    """Schema for creating a BazaarBucks payment"""
    model_config = ConfigDict(populate_by_name=True)


class BazaarBucksPayment(BazaarBucksPaymentBase):
    """Schema for BazaarBucks payment response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class StripePaymentBase(BaseModel):
    """Base Stripe payment schema"""
    agent_id: str = Field(alias="agentId", serialization_alias="agentId")
    vendor: str
    amount: float
    status: str = "completed"
    type: str = "card_spend"


class StripePaymentCreate(StripePaymentBase):
    """Schema for creating a Stripe payment"""
    model_config = ConfigDict(populate_by_name=True)


class StripePayment(StripePaymentBase):
    """Schema for Stripe payment response (matches UI TypeScript schema)"""
    id: str
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
