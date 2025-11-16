# Wallet Balance Library - Complete Documentation

Python library for querying USDC token balances on Coinbase Base blockchain using direct RPC calls.

## Installation

```bash
pip install web3 python-dotenv
```

Or add to your `requirements.txt`:
```
web3>=6.15.0
python-dotenv>=1.0.0
```

## How to Use

### Method 1: Quick One-Line Balance Query

```python
from wallet_client import get_wallet_balance

result = get_wallet_balance(
    wallet_address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6"
)

print(result["message"] if "message" in result else result)
```

### Method 2: Using the Client Class (Recommended)

```python
from wallet_client import WalletBalanceClient

# Step 1: Initialize the client
client = WalletBalanceClient()

# Step 2: Get USDC balance
result = client.get_usdc_balance(
    wallet_address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6"
)

# Step 3: Check the result
if result["success"]:
    print("✅ Balance retrieved successfully!")
    print(f"   Balance: {result['balance']} USDC")
    print(f"   Wallet: {result['wallet_address']}")
else:
    print("❌ Failed to get balance")
    print(f"   Error: {result.get('error', 'Unknown error')}")
```

### Method 3: Using Environment Variables

Create a `.env` file:
```env
BASE_RPC_URL=https://mainnet.base.org
```

Then in your code:
```python
import os
from dotenv import load_dotenv
from wallet_client import WalletBalanceClient

load_dotenv()

client = WalletBalanceClient(rpc_url=os.getenv("BASE_RPC_URL"))
result = client.get_usdc_balance(
    wallet_address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6"
)
print(f"Balance: {result['balance']} USDC")
```

## API Reference

### `WalletBalanceClient(rpc_url: Optional[str] = None)`

Main client class for interacting with Base blockchain.

#### Methods

**`get_usdc_balance(wallet_address: str)`**
- Get USDC balance for any wallet address on Base
- Returns: `{"success": True, "balance": 100.5, "wallet_address": "...", ...}`

**`get_native_balance(wallet_address: str)`**
- Get native ETH balance for any wallet address on Base
- Returns: Balance result with ETH amount

### Example 1: Check Balance

```python
from wallet_client import WalletBalanceClient

client = WalletBalanceClient()
result = client.get_usdc_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")

if result["success"]:
    print(f"Balance: {result['balance']} USDC")
```

### Example 2: Check Multiple Wallets

```python
from wallet_client import WalletBalanceClient

client = WalletBalanceClient()

wallets = [
    "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
]

for wallet in wallets:
    result = client.get_usdc_balance(wallet)
    if result["success"]:
        print(f"{result['wallet_address']}: {result['balance']} USDC")
```

### Example 3: Custom RPC Endpoint

```python
from wallet_client import WalletBalanceClient

# Use Coinbase Base Node or custom RPC
client = WalletBalanceClient(rpc_url="https://mainnet.base.org")
result = client.get_usdc_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
```

## Response Format

### Success Response

```python
{
    "success": True,
    "balance": 100.5,              # USDC amount (float)
    "balance_raw": "100500000",     # Raw balance in smallest unit
    "wallet_address": "0xE1E1D4503105D4B0466419FF173900031E7E5ED6",  # Checksum format
    "chain": "base",
    "token": "USDC"
}
```

### Error Response

```python
{
    "success": False,
    "balance": 0.0,
    "balance_raw": "0",
    "wallet_address": "0x...",
    "error": "Error message describing what went wrong"
}
```

## Configuration

### USDC Contract on Base

- **Contract Address**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Decimals**: 6
- **Token Standard**: ERC-20

### Base RPC Endpoints

- **Public**: `https://mainnet.base.org`
- **Coinbase Base Node**: (if you have access)
- **Alchemy**: `https://base-mainnet.g.alchemy.com/v2/YOUR_API_KEY`
- **Infura**: `https://base-mainnet.infura.io/v3/YOUR_API_KEY`

## Error Handling

The library handles various error scenarios:

- **Invalid Address**: Returns error if address format is invalid
- **Network Errors**: Handles connection timeouts and RPC failures
- **Contract Errors**: Handles contract call failures gracefully

Always check the `success` field before using the result:

```python
result = client.get_usdc_balance(address)
if result["success"]:
    # Use result["balance"]
else:
    # Handle error: result["error"]
```

## Testing

Run the example file to test:

```bash
python example_usage.py
```

## Integration Examples

### FastAPI Endpoint

```python
from fastapi import APIRouter
from wallet_balance.wallet_client import WalletBalanceClient

router = APIRouter()
client = WalletBalanceClient()

@router.get("/wallet/{address}/balance")
async def get_balance(address: str):
    result = client.get_usdc_balance(address)
    return result
```

### Standalone Script

```python
#!/usr/bin/env python3
from wallet_client import get_wallet_balance
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <wallet_address>")
    sys.exit(1)

address = sys.argv[1]
result = get_wallet_balance(address)

if result["success"]:
    print(f"Balance: {result['balance']} USDC")
else:
    print(f"Error: {result.get('error')}")
    sys.exit(1)
```

## Notes

- All wallet addresses are automatically converted to checksum format (EIP-55)
- USDC balances are returned with 6 decimal precision
- The library uses direct RPC calls to Base blockchain
- Supports both USDC (ERC-20) and native ETH balance queries
- Thread-safe for concurrent requests (create separate client instances)

