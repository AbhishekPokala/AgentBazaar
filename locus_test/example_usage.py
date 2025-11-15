#!/usr/bin/env python3
"""
Example usage of Locus Client Library
"""

from locus_client import LocusClient, send_transaction
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_1_simple():
    """Simple one-line transaction"""
    api_key = os.getenv("LOCUS_API_KEY", "your_api_key_here")
    result = send_transaction(
        api_key=api_key,
        to_address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        amount=0.1,
        memo="Payment from Python"
    )
    print(result)


def example_2_client():
    """Using the client class for multiple operations"""
    api_key = os.getenv("LOCUS_API_KEY", "your_api_key_here")
    client = LocusClient(api_key)
    
    # Get payment context
    print("📊 Payment Context:")
    context = client.get_payment_context()
    print(context.get("message", ""))
    
    # Send transaction
    print("\n💸 Sending Transaction:")
    result = client.send_to_address(
        address="0xe1e1d4503105d4b0466419ff173900031e7e5ed6",
        amount=0.1,
        memo="Hackathon payment"
    )
    print(result.get("message", ""))


def example_3_list_tools():
    """List all available tools"""
    api_key = os.getenv("LOCUS_API_KEY", "your_api_key_here")
    client = LocusClient(api_key)
    
    tools = client.list_tools()
    print(f"Available tools ({len(tools)}):")
    for tool in tools:
        print(f"  - {tool.get('name', 'Unknown')}")


if __name__ == "__main__":
    print("=" * 60)
    print("Locus Client Examples")
    print("=" * 60)
    
    # Uncomment the example you want to run:
    # example_1_simple()
    # example_2_client()
    # example_3_list_tools()

