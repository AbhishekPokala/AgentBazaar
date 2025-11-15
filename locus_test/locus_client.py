"""
Locus MCP Client Library
Simple Python library for interacting with Locus MCP server
"""

import json
import requests
from typing import Optional, Dict, Any


class LocusClient:
    """Client for interacting with Locus MCP server"""
    
    MCP_URL = "https://mcp.paywithlocus.com/mcp"
    
    def __init__(self, api_key: str):
        """
        Initialize Locus client
        
        Args:
            api_key: Your Locus API key (starts with 'locus_')
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
    
    def _call_mcp(self, method: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Internal method to call MCP server
        
        Args:
            method: MCP method name (e.g., 'tools/list', 'tools/call')
            params: Method parameters
            
        Returns:
            Response data as dictionary
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        response = requests.post(
            self.MCP_URL,
            headers=self.headers,
            json=payload,
            timeout=30,
            stream=True
        )
        response.raise_for_status()
        
        # Handle SSE streaming response
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/event-stream' in content_type:
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            return json.loads(line_str[6:])  # Remove 'data: ' prefix
                        except json.JSONDecodeError:
                            continue
            raise ValueError("No valid JSON data found in SSE stream")
        else:
            return response.json()
    
    def list_tools(self) -> list:
        """
        List all available tools from Locus MCP server
        
        Returns:
            List of available tools
        """
        result = self._call_mcp("tools/list")
        return result.get("result", {}).get("tools", [])
    
    def send_to_address(self, address: str, amount: float, memo: str = "") -> Dict[str, Any]:
        """
        Send USDC to a wallet address
        
        Args:
            address: Recipient wallet address (0x...)
            amount: Amount in USDC to send
            memo: Optional payment memo/description
            
        Returns:
            Transaction result with status and transaction ID
        """
        result = self._call_mcp("tools/call", {
            "name": "send_to_address",
            "arguments": {
                "address": address,
                "amount": float(amount),
                "memo": memo
            }
        })
        
        # Extract text content from response
        response_data = result.get("result", {})
        content = response_data.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            return {"success": True, "message": text, "data": response_data}
        
        return {"success": True, "data": response_data}
    
    def send_to_contact(self, contact_number: int, amount: float, memo: str = "") -> Dict[str, Any]:
        """
        Send USDC to a whitelisted contact
        
        Args:
            contact_number: Contact number from whitelisted contacts (1, 2, 3...)
            amount: Amount in USDC to send
            memo: Payment memo/description
            
        Returns:
            Transaction result
        """
        result = self._call_mcp("tools/call", {
            "name": "send_to_contact",
            "arguments": {
                "contact_number": contact_number,
                "amount": float(amount),
                "memo": memo
            }
        })
        
        response_data = result.get("result", {})
        content = response_data.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            return {"success": True, "message": text, "data": response_data}
        
        return {"success": True, "data": response_data}
    
    def send_to_email(self, email: str, amount: float, memo: str = "") -> Dict[str, Any]:
        """
        Send USDC via escrow to an email address
        
        Args:
            email: Recipient email address
            amount: Amount in USDC to send
            memo: Optional payment memo
            
        Returns:
            Transaction result with escrow ID
        """
        result = self._call_mcp("tools/call", {
            "name": "send_to_email",
            "arguments": {
                "email": email,
                "amount": float(amount),
                "memo": memo
            }
        })
        
        response_data = result.get("result", {})
        content = response_data.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            return {"success": True, "message": text, "data": response_data}
        
        return {"success": True, "data": response_data}
    
    def get_payment_context(self) -> Dict[str, Any]:
        """
        Get payment context including budget status and whitelisted contacts
        
        Returns:
            Payment context information
        """
        result = self._call_mcp("tools/call", {
            "name": "get_payment_context",
            "arguments": {}
        })
        
        response_data = result.get("result", {})
        content = response_data.get("content", [])
        if content and isinstance(content, list):
            text = content[0].get("text", "")
            return {"success": True, "message": text, "data": response_data}
        
        return {"success": True, "data": response_data}


# Convenience function for quick usage
def send_transaction(api_key: str, to_address: str, amount: float, memo: str = "") -> Dict[str, Any]:
    """
    Quick function to send a transaction
    
    Args:
        api_key: Locus API key
        to_address: Recipient wallet address
        amount: Amount in USDC
        memo: Optional memo
        
    Returns:
        Transaction result
    """
    client = LocusClient(api_key)
    return client.send_to_address(to_address, amount, memo)

