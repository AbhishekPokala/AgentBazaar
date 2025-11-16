#!/bin/bash

# Start HubChat API Server
# This exposes HubChat via HTTP for ChatGPT Actions

echo "🚀 Starting HubChat Orchestrator API..."
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
echo "🎯 HubChat API will be available at:"
echo "   • API: http://localhost:8000"
echo "   • Docs: http://localhost:8000/docs"
echo "   • OpenAPI: http://localhost:8000/openapi.json"
echo "=" * 60
echo ""

cd hubchat
python api.py

