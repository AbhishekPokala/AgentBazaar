"""
Example usage of the wallet balance library
"""

from wallet_client import WalletBalanceClient, get_wallet_balance


def example_1_simple():
    """Simple one-line usage"""
    result = get_wallet_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    
    if result["success"]:
        print(f"✅ Balance: {result['balance']} USDC")
        print(f"   Wallet: {result['wallet_address']}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def example_2_client():
    """Using the client class (recommended for multiple queries)"""
    client = WalletBalanceClient()
    
    # Query multiple wallets
    wallets = [
        "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    ]
    
    for wallet in wallets:
        result = client.get_usdc_balance(wallet)
        if result["success"]:
            print(f"✅ {result['wallet_address']}: {result['balance']} USDC")
        else:
            print(f"❌ {wallet}: {result.get('error', 'Unknown error')}")


def example_3_custom_rpc():
    """Using custom RPC endpoint"""
    # You can use Coinbase Base Node or any other Base RPC
    custom_rpc = "https://mainnet.base.org"  # or your Coinbase Base Node URL
    
    client = WalletBalanceClient(rpc_url=custom_rpc)
    result = client.get_usdc_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    print(result)


def example_4_native_balance():
    """Get native ETH balance on Base"""
    client = WalletBalanceClient()
    result = client.get_native_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    
    if result["success"]:
        print(f"✅ ETH Balance: {result['balance']} ETH")
    else:
        print(f"❌ Error: {result.get('error')}")


if __name__ == "__main__":
    print("=== Example 1: Simple Usage ===")
    example_1_simple()
    
    print("\n=== Example 2: Client Class ===")
    example_2_client()
    
    print("\n=== Example 3: Custom RPC ===")
    example_3_custom_rpc()
    
    print("\n=== Example 4: Native ETH Balance ===")
    example_4_native_balance()

