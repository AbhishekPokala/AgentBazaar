"""
Standalone test script for wallet balance library
"""

from wallet_client import WalletBalanceClient, get_wallet_balance


def test_simple_balance():
    """Test simple balance query"""
    print("Testing simple balance query...")
    result = get_wallet_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    
    assert "success" in result, "Result should have 'success' field"
    print(f"✅ Simple test passed: success={result['success']}")
    if result["success"]:
        print(f"   Balance: {result['balance']} USDC")


def test_client_class():
    """Test client class usage"""
    print("\nTesting client class...")
    client = WalletBalanceClient()
    
    result = client.get_usdc_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    assert "success" in result, "Result should have 'success' field"
    print(f"✅ Client class test passed: success={result['success']}")


def test_native_balance():
    """Test native ETH balance"""
    print("\nTesting native ETH balance...")
    client = WalletBalanceClient()
    
    result = client.get_native_balance("0xe1e1d4503105d4b0466419ff173900031e7e5ed6")
    assert "success" in result, "Result should have 'success' field"
    print(f"✅ Native balance test passed: success={result['success']}")
    if result["success"]:
        print(f"   ETH Balance: {result['balance']} ETH")


def test_invalid_address():
    """Test with invalid address"""
    print("\nTesting invalid address handling...")
    result = get_wallet_balance("invalid_address")
    
    assert result["success"] == False, "Invalid address should return success=False"
    assert "error" in result, "Error should be present in result"
    print(f"✅ Invalid address test passed: {result['error']}")


def test_multiple_wallets():
    """Test querying multiple wallets"""
    print("\nTesting multiple wallet queries...")
    client = WalletBalanceClient()
    
    wallets = [
        "0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    ]
    
    for wallet in wallets:
        result = client.get_usdc_balance(wallet)
        assert "success" in result, "Result should have 'success' field"
        print(f"   Wallet {wallet[:10]}...: success={result['success']}")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Wallet Balance Library - Standalone Tests")
    print("=" * 60)
    
    try:
        test_simple_balance()
        test_client_class()
        test_native_balance()
        test_invalid_address()
        test_multiple_wallets()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

