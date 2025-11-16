"""
Wallet balance endpoints
"""
import sys
import os
from fastapi import APIRouter, HTTPException

# Add wallet_balance to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

router = APIRouter()

# Customer wallet address (hardcoded for demo)
CUSTOMER_WALLET = "0xf76b5a90bfa57aee275137b4e96cbc74e3933d19"


@router.get("/api/wallet/balance")
async def get_wallet_balance():
    """
    Get customer's USDC balance from Base blockchain
    """
    try:
        from wallet_balance.wallet_client import get_wallet_balance
        
        result = get_wallet_balance(CUSTOMER_WALLET)
        
        return result
    except ImportError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Wallet balance library not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching wallet balance: {str(e)}"
        )


@router.get("/api/wallet/address")
async def get_wallet_address():
    """
    Get customer wallet address
    """
    return {
        "wallet_address": CUSTOMER_WALLET,
        "network": "base",
        "token": "USDC"
    }
