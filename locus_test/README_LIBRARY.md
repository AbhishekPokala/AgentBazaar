# Locus Python Client Library

Simple Python library for sending transactions via Locus MCP server.

## Installation

```bash
pip install requests python-dotenv
```

Or add to your `requirements.txt`:
```
requests>=2.31.0
python-dotenv>=1.0.0
```

## How to Use

### Method 1: Quick One-Line Transaction

```python
from locus_client import send_transaction

result = send_transaction(
    api_key="locus_dev_your_api_key_here",
    to_address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    amount=0.1,
    memo="Payment from Python"
)

print(result["message"])
```

### Method 2: Using the Client Class (Recommended)

```python
from locus_client import LocusClient

# Step 1: Initialize the client with your API key
client = LocusClient(api_key="locus_dev_your_api_key_here")

# Step 2: Send a transaction
result = client.send_to_address(
    address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    amount=0.1,
    memo="Payment from Python"
)

# Step 3: Check the result
if result["success"]:
    print("✅ Transaction successful!")
    print(result["message"])
else:
    print("❌ Transaction failed")
```

### Method 3: Using Environment Variables

Create a `.env` file:
```env
LOCUS_API_KEY=locus_dev_your_api_key_here
```

Then in your code:
```python
import os
from dotenv import load_dotenv
from locus_client import LocusClient

load_dotenv()

client = LocusClient(api_key=os.getenv("LOCUS_API_KEY"))
result = client.send_to_address(
    address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    amount=0.1
)
print(result["message"])
```

## API Reference

### `LocusClient(api_key: str)`

Main client class for interacting with Locus MCP server.

#### Methods

**`send_to_address(address: str, amount: float, memo: str = "")`**
- Send USDC to any wallet address
- Returns: `{"success": True, "message": "...", "data": {...}}`

**`send_to_contact(contact_number: int, amount: float, memo: str = "")`**
- Send USDC to a whitelisted contact
- Returns: Transaction result

**`send_to_email(email: str, amount: float, memo: str = "")`**
- Send USDC via escrow to an email address
- Returns: Transaction result with escrow ID

**`get_payment_context()`**
- Get payment context (balance, whitelisted contacts, etc.)
- Returns: Payment context information

**`list_tools()`**
- List all available tools from MCP server
- Returns: List of tool definitions

## Complete Examples

### Example 1: Send Transaction to Address

```python
from locus_client import LocusClient

# Initialize client
client = LocusClient(api_key="locus_dev_your_api_key")

# Send 0.1 USDC to an address
result = client.send_to_address(
    address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    amount=0.1,
    memo="Payment from Python"
)

# Print result
print(result["message"])
# Output: ✅ Payment queued successfully! Transaction ID: ...
```

### Example 2: Check Balance and Send

```python
from locus_client import LocusClient

client = LocusClient(api_key="locus_dev_your_api_key")

# Step 1: Check payment context (balance, contacts, etc.)
print("Checking payment context...")
context = client.get_payment_context()
print(context["message"])

# Step 2: Send payment
print("\nSending payment...")
result = client.send_to_address(
    address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
    amount=0.1,
    memo="Payment"
)

print(result["message"])
```

### Example 3: Send to Whitelisted Contact

```python
from locus_client import LocusClient

client = LocusClient(api_key="locus_dev_your_api_key")

# Send to contact #1 from your whitelist
result = client.send_to_contact(
    contact_number=1,  # Contact number from whitelist
    amount=0.1,
    memo="Lunch payment"
)

print(result["message"])
```

### Example 4: Send via Email (Escrow)

```python
from locus_client import LocusClient

client = LocusClient(api_key="locus_dev_your_api_key")

# Send to email - creates escrow, recipient gets email to claim
result = client.send_to_email(
    email="recipient@example.com",
    amount=0.1,
    memo="Payment for services"
)

print(result["message"])
```

### Example 5: List Available Tools

```python
from locus_client import LocusClient

client = LocusClient(api_key="locus_dev_your_api_key")

# List all available tools
tools = client.list_tools()
print(f"Available tools ({len(tools)}):")
for tool in tools:
    print(f"  - {tool.get('name', 'Unknown')}")
    if tool.get('description'):
        print(f"    {tool.get('description')[:60]}...")
```

## Error Handling

```python
from locus_client import LocusClient
import requests

client = LocusClient(api_key="locus_dev_your_api_key")

try:
    result = client.send_to_address(
        address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        amount=0.1,
        memo="Test"
    )
    
    if result["success"]:
        print("✅ Transaction successful!")
        print(result["message"])
    else:
        print("❌ Transaction failed")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Network error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
    print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
except Exception as e:
    print(f"❌ Error: {e}")
```

## Quick Reference

### Import the Library

```python
from locus_client import LocusClient, send_transaction
```

### Initialize Client

```python
client = LocusClient(api_key="locus_dev_your_api_key")
```

### Available Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `send_to_address()` | Send USDC to wallet address | `address`, `amount`, `memo` |
| `send_to_contact()` | Send to whitelisted contact | `contact_number`, `amount`, `memo` |
| `send_to_email()` | Send via email escrow | `email`, `amount`, `memo` |
| `get_payment_context()` | Get balance & contacts | None |
| `list_tools()` | List available tools | None |

### Response Format

All methods return a dictionary:
```python
{
    "success": True,
    "message": "✅ Payment queued successfully!...",
    "data": {...}  # Full response data
}
```

## Requirements

- Python 3.7+
- `requests` library
- `python-dotenv` (optional, for .env file support)

## License

MIT

## Support

For issues or questions, check the [Locus MCP Documentation](https://docs.paywithlocus.com/mcp-spec)

