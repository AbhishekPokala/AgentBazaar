#!/bin/bash

# Start HubChat MCP Server
# For use with ChatGPT Desktop

echo "🚀 Starting HubChat MCP Server..."
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ERROR: ANTHROPIC_API_KEY not set"
    echo "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if agents are running
echo "🔍 Checking if agents are running..."
if ! curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "⚠️  WARNING: Agents don't seem to be running"
    echo "   Start them first with: ./start_all_services.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "=" * 60
echo "🎯 HubChat MCP Server"
echo "=" * 60
echo "   Protocol: Model Context Protocol"
echo "   Mode: ChatGPT Desktop Integration"
echo "   Tools: orchestrate_task, list_available_agents"
echo "=" * 60
echo ""
echo "💡 Add to ChatGPT Desktop config:"
echo "   See hubchat/MCP_SETUP.md for instructions"
echo ""

cd hubchat
python mcp_server.py

