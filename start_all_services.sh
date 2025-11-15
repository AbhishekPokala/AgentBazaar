#!/bin/bash
# Script to start all services in separate terminal windows/tabs
# Usage: ./start_all_services.sh

set -e

echo "🚀 Starting Agentic Marketplace Services..."
echo ""

# Check if API server is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Warning: Port 8000 is already in use. API server may already be running."
fi

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get absolute path of project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to start a service in the background
start_service() {
    local name=$1
    local port=$2
    local path=$3
    local cmd=$4

    echo -e "${BLUE}Starting $name on port $port...${NC}"
    cd "$path"
    $cmd > "${PROJECT_ROOT}/logs/${name}.log" 2>&1 &
    echo $! > "${PROJECT_ROOT}/logs/${name}.pid"
    cd - > /dev/null
    sleep 1
}

# Create logs directory
mkdir -p "${PROJECT_ROOT}/logs"

echo "Starting services..."
echo ""

# Start Agent Services (NO API SERVER - agents are standalone)
echo -e "${GREEN}[1/6] Summarizer Agent (Port 8001) - Claude-powered${NC}"
start_service "summarizer" 8001 "services/summarizer" "python app.py"

echo -e "${GREEN}[2/6] Translator Agent (Port 8002) - Claude-powered${NC}"
start_service "translator" 8002 "services/translator" "python app.py"

echo -e "${GREEN}[3/6] Search Agent (Port 8003) - Claude-powered${NC}"
start_service "search" 8003 "services/search" "python app.py"

echo -e "${GREEN}[4/6] Mock Busy Agent (Port 8004)${NC}"
start_service "mock_busy" 8004 "services/mock_busy" "python app.py"

echo -e "${GREEN}[5/6] Mock High Price Agent (Port 8005)${NC}"
start_service "mock_highprice" 8005 "services/mock_highprice" "python app.py"

echo -e "${GREEN}[6/6] Mock Negotiator Agent (Port 8006)${NC}"
start_service "mock_negotiator" 8006 "services/mock_negotiator" "python app.py"

# Wait for all services to start
sleep 3

echo ""
echo "✅ All services started!"
echo ""
echo "📋 Service Status:"
echo "  REAL AGENTS (Claude-powered):"
echo "  • Summarizer:        http://localhost:8001 ✨"
echo "  • Translator:        http://localhost:8002 ✨"
echo "  • Search:            http://localhost:8003 ✨"
echo ""
echo "  MOCK AGENTS (Test scenarios):"
echo "  • Mock Busy:         http://localhost:8004"
echo "  • Mock High Price:   http://localhost:8005"
echo "  • Mock Negotiator:   http://localhost:8006"
echo ""
echo "📝 Logs are in: ./logs/"
echo "🛑 To stop all services, run: ./stop_all_services.sh"
echo ""
echo "🧪 Test individual agents:"
echo "  curl http://localhost:8001/health"
echo "  curl -X POST http://localhost:8001/execute -H 'Content-Type: application/json' -d '{\"text\":\"AI is transforming technology.\"}'"
echo ""
echo "🤖 Test with HubChat orchestrator:"
echo "  cd hubchat && python example_usage.py"

