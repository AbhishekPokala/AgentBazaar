"""
Payment API Routes (Stub Implementation for Phase 5)
"""
from fastapi import APIRouter
from typing import List

from models.payment import BazaarBucksPayment, StripePayment

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.get("/bazaarbucks", response_model=List[BazaarBucksPayment])
async def get_bazaarbucks_payments():
    """
    Get all BazaarBucks payments
    
    NOTE: This is a stub implementation. Returns empty array.
    Full payment tracking will be implemented in Phase 5.
    """
    return []


@router.get("/stripe", response_model=List[StripePayment])
async def get_stripe_payments():
    """
    Get all Stripe payments
    
    NOTE: This is a stub implementation. Returns empty array.
    Full payment tracking will be implemented in Phase 5.
    """
    return []
