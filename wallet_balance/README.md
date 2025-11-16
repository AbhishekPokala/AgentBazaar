# Wallet Balance Library

Python library for querying USDC token balances on Coinbase Base blockchain using direct RPC calls.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Optional: Create a `.env` file** in this directory with custom RPC URL:
   ```
   BASE_RPC_URL=https://mainnet.base.org
   ```
   Or use Coinbase Base Node URL if you have access.

3. **Run examples:**
   ```bash
   python example_usage.py
   ```

## Quick Start

### Method 1: Simple One-Line Usage

```python
from wallet_client import get_wallet_balance

result = get_wallet_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")

if result["success"]:
    print(f"Balance: {result['balance']} USDC")
else:
    print(f"Error: {result['error']}")
```

### Method 2: Using the Client Class (Recommended)

```python
from wallet_client import WalletBalanceClient

# Initialize client
client = WalletBalanceClient()

# Get USDC balance
result = client.get_usdc_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")

if result["success"]:
    print(f"Balance: {result['balance']} USDC")
    print(f"Raw balance: {result['balance_raw']}")
    print(f"Wallet: {result['wallet_address']}")
```

## API Reference

### `WalletBalanceClient(rpc_url: Optional[str] = None)`

Main client class for querying wallet balances.

**Parameters:**
- `rpc_url` (optional): Base RPC endpoint URL. Defaults to `BASE_RPC_URL` env var or public Base mainnet.

**Methods:**

#### `get_usdc_balance(wallet_address: str) -> Dict[str, Any]`

Get USDC balance for a wallet address on Base.

**Returns:**
```python
{
    "success": True,
    "balance": 100.5,  # USDC amount (float)
    "balance_raw": "100500000",  # Raw balance in smallest unit
    "wallet_address": "0xE1E1D4503105D4B0466419FF173900031E7E5ED6",  # Checksum format
    "chain": "base",
    "token": "USDC"
}
```

#### `get_native_balance(wallet_address: str) -> Dict[str, Any]`

Get native ETH balance for a wallet address on Base.

**Returns:**
```python
{
    "success": True,
    "balance": 0.5,  # ETH amount (float)
    "balance_raw": "500000000000000000",  # Raw balance in wei
    "wallet_address": "0xE1E1D4503105D4B0466419FF173900031E7E5ED6",
    "chain": "base",
    "token": "ETH"
}
```

### `get_wallet_balance(wallet_address: str, rpc_url: Optional[str] = None) -> Dict[str, Any]`

Convenience function for quick USDC balance queries.

## Configuration

### USDC Contract Address

The library uses the official USDC contract on Base:
- **Address**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Decimals**: 6

### Base RPC Endpoints

Default: `https://mainnet.base.org` (public)

For production, consider using:
- Coinbase Base Node (if you have access)
- Alchemy Base API
- Infura Base API
- QuickNode Base API

## Error Handling

All methods return a dictionary with a `success` field. On error:

```python
{
    "success": False,
    "balance": 0.0,
    "balance_raw": "0",
    "wallet_address": "0x...",
    "error": "Error message describing what went wrong"
}
```

## Usage in Other Projects

To use this library in other parts of the codebase:

```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'wallet_balance'))

from wallet_client import WalletBalanceClient, get_wallet_balance

# Use the library
result = get_wallet_balance("0x...")
```

Or in FastAPI:

```python
from wallet_balance.wallet_client import WalletBalanceClient

client = WalletBalanceClient()

@router.get("/wallet/{address}/balance")
async def get_balance(address: str):
    result = client.get_usdc_balance(address)
    return result
```

## Notes

- All addresses are automatically converted to checksum format
- USDC balances are returned with 6 decimal precision
- The library handles connection errors gracefully
- Supports both USDC (ERC-20) and native ETH balances

