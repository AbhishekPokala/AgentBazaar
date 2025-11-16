"""
Wallet Balance Library for Base Blockchain
Queries USDC token balance on Coinbase Base network using direct RPC calls
"""

import os
from typing import Dict, Any, Optional
from decimal import Decimal
from web3 import Web3
from web3.exceptions import ContractLogicError


class WalletBalanceClient:
    """Client for querying wallet balances on Base blockchain"""
    
    # Base mainnet RPC endpoint (Coinbase Base Node)
    BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
    
    # USDC contract address on Base
    USDC_CONTRACT_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    
    # USDC has 6 decimals
    USDC_DECIMALS = 6
    
    # ERC-20 balanceOf function ABI
    ERC20_BALANCE_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    
    def __init__(self, rpc_url: Optional[str] = None):
        """
        Initialize wallet balance client
        
        Args:
            rpc_url: Optional Base RPC endpoint URL. 
                    Defaults to BASE_RPC_URL env var or public Base mainnet
        """
        self.rpc_url = rpc_url or self.BASE_RPC_URL
        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Verify connection
        if not self.web3.is_connected():
            raise ConnectionError(f"Failed to connect to Base RPC: {self.rpc_url}")
        
        # Initialize USDC contract
        self.usdc_contract = self.web3.eth.contract(
            address=Web3.to_checksum_address(self.USDC_CONTRACT_ADDRESS),
            abi=self.ERC20_BALANCE_ABI
        )
    
    def get_usdc_balance(self, wallet_address: str) -> Dict[str, Any]:
        """
        Get USDC balance for a wallet address on Base
        
        Args:
            wallet_address: Ethereum wallet address (0x...)
            
        Returns:
            Dictionary with:
            - success: bool
            - balance: float (USDC amount)
            - balance_raw: str (raw balance in wei/smallest unit)
            - wallet_address: str (normalized address)
            - error: str (if any)
        """
        try:
            # Normalize address to checksum format
            checksum_address = Web3.to_checksum_address(wallet_address)
            
            # Query balance from USDC contract
            balance_raw = self.usdc_contract.functions.balanceOf(checksum_address).call()
            
            # Convert from smallest unit to USDC (6 decimals)
            balance_usdc = Decimal(balance_raw) / Decimal(10 ** self.USDC_DECIMALS)
            
            return {
                "success": True,
                "balance": float(balance_usdc),
                "balance_raw": str(balance_raw),
                "wallet_address": checksum_address,
                "chain": "base",
                "token": "USDC"
            }
            
        except ValueError as e:
            # Invalid address format
            return {
                "success": False,
                "balance": 0.0,
                "balance_raw": "0",
                "wallet_address": wallet_address,
                "error": f"Invalid wallet address: {str(e)}"
            }
        except ContractLogicError as e:
            # Contract call error
            return {
                "success": False,
                "balance": 0.0,
                "balance_raw": "0",
                "wallet_address": wallet_address,
                "error": f"Contract error: {str(e)}"
            }
        except Exception as e:
            # Other errors (network, connection, etc.)
            return {
                "success": False,
                "balance": 0.0,
                "balance_raw": "0",
                "wallet_address": wallet_address,
                "error": f"Error querying balance: {str(e)}"
            }
    
    def get_native_balance(self, wallet_address: str) -> Dict[str, Any]:
        """
        Get native ETH balance for a wallet address on Base
        
        Args:
            wallet_address: Ethereum wallet address (0x...)
            
        Returns:
            Dictionary with balance in ETH
        """
        try:
            checksum_address = Web3.to_checksum_address(wallet_address)
            balance_wei = self.web3.eth.get_balance(checksum_address)
            balance_eth = Web3.from_wei(balance_wei, 'ether')
            
            return {
                "success": True,
                "balance": float(balance_eth),
                "balance_raw": str(balance_wei),
                "wallet_address": checksum_address,
                "chain": "base",
                "token": "ETH"
            }
        except Exception as e:
            return {
                "success": False,
                "balance": 0.0,
                "balance_raw": "0",
                "wallet_address": wallet_address,
                "error": f"Error querying native balance: {str(e)}"
            }


# Convenience function for quick usage
def get_wallet_balance(wallet_address: str, rpc_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick function to get USDC balance for a wallet address
    
    Args:
        wallet_address: Ethereum wallet address (0x...)
        rpc_url: Optional Base RPC endpoint URL
        
    Returns:
        Dictionary with balance information
    """
    client = WalletBalanceClient(rpc_url=rpc_url)
    return client.get_usdc_balance(wallet_address)

