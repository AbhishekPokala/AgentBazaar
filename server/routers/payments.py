"""
Payment API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from db.database import get_db
from db.repositories.message_repository import MessageRepository
from models.payment import BazaarBucksPayment, StripePayment

router = APIRouter(prefix="/api/payments", tags=["payments"])


class LocusPayment(BaseModel):
    """Locus blockchain payment"""
    id: str
    timestamp: datetime
    agent_id: str
    agent_name: str
    amount: float
    memo: str
    recipient_wallet: str
    network: str = "base"
    token: str = "USDC"


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


@router.get("/locus", response_model=List[LocusPayment])
async def get_locus_payments(
    limit: int = 100,
    session: AsyncSession = Depends(get_db)
):
    """
    Get Locus blockchain payments extracted from orchestration data
    """
    try:
        message_repo = MessageRepository(session)
        
        # Fetch more messages to ensure we collect enough payments
        # (Each message can have multiple payments, so fetch 10x the limit)
        messages = await message_repo.get_assistant_with_orchestration(limit=limit * 10)
        
        # Extract payments from orchestration_data
        payments = []
        for msg in messages:
            orchestration = msg.orchestration_data
            payments_made = orchestration.get("payments_made", [])
            
            for payment in payments_made:
                payments.append(LocusPayment(
                    id=f"{msg.id}-{payment.get('agent_id', 'unknown')}",
                    timestamp=msg.created_at,
                    agent_id=payment.get("agent_id", "unknown"),
                    agent_name=payment.get("agent_id", "unknown").replace("_", " ").title(),
                    amount=payment.get("amount", 0.0),
                    memo=payment.get("memo", ""),
                    recipient_wallet=payment.get("recipient", "unknown"),
                    network="base",
                    token="USDC"
                ))
                
                # Stop collecting if we've reached the desired payment count
                if len(payments) >= limit:
                    break
            
            if len(payments) >= limit:
                break
        
        # Return up to the requested number of payments
        return payments[:limit]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching Locus payments: {str(e)}"
        )
