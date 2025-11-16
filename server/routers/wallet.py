"""
Wallet balance endpoints
"""
import sys
import os
from fastapi import APIRouter
import logging

# Add wallet_balance to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

router = APIRouter()
logger = logging.getLogger(__name__)

# Customer wallet address (hardcoded for demo)
CUSTOMER_WALLET = "0xf76b5a90bfa57aee275137b4e96cbc74e3933d19"


@router.get("/api/wallet/balance")
async def get_wallet_balance():
    """
    Get customer's USDC balance from Base blockchain.
    Returns mock data if wallet_balance library is not available.
    """
    try:
        from wallet_balance.wallet_client import get_wallet_balance
        
        result = get_wallet_balance(CUSTOMER_WALLET)
        
        return result
    except ImportError as e:
        # Return mock balance if library not available
        logger.warning(f"Wallet balance library not available, returning mock data: {e}")
        return {
            "success": True,
            "balance": 100.0,  # Mock balance for demo
            "wallet_address": CUSTOMER_WALLET,
            "network": "base",
            "token": "USDC",
            "mock": True
        }
    except Exception as e:
        # Return mock balance on any error
        logger.error(f"Error fetching wallet balance: {e}")
        return {
            "success": True,
            "balance": 100.0,  # Mock balance on error
            "wallet_address": CUSTOMER_WALLET,
            "network": "base",
            "token": "USDC",
            "mock": True
        }


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
