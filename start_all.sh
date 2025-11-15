#!/bin/bash
# Comprehensive startup script for Agent Bazaar
# Starts: Frontend (Vite), Backend API (FastAPI), and all Agent Services
# Usage: ./start_all.sh

set -e

echo "🚀 Starting Agent Bazaar - All Services..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get absolute path of project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create logs directory
mkdir -p "${PROJECT_ROOT}/logs"

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${RED}⚠️  Warning: Port $port is already in use!${NC}"
        return 1
    fi
    return 0
}

# Function to start a service in the background
start_service() {
    local name=$1
    local port=$2
    local path=$3
    local cmd=$4

    echo -e "${BLUE}Starting $name on port $port...${NC}"
    cd "$path"
    eval "$cmd" > "${PROJECT_ROOT}/logs/${name}.log" 2>&1 &
    echo $! > "${PROJECT_ROOT}/logs/${name}.pid"
    cd - > /dev/null
    sleep 1
}

# Check critical ports
echo "Checking ports..."
check_port 5173 || echo -e "${YELLOW}  Frontend (Vite) may already be running${NC}"
check_port 8000 || echo -e "${YELLOW}  Backend API may already be running${NC}"
check_port 8001 || echo -e "${YELLOW}  Agent service on 8001 may already be running${NC}"
echo ""

echo "Starting all services..."
echo ""

# [1/9] Start Frontend (Vite dev server)
echo -e "${GREEN}[1/9] Frontend (Vite Dev Server - Port 5173)${NC}"
start_service "frontend" 5173 "${PROJECT_ROOT}/ui" "npx vite"

# [2/9] Start Backend API (FastAPI)
echo -e "${GREEN}[2/9] Backend API (FastAPI - Port 8000)${NC}"
start_service "backend_api" 8000 "${PROJECT_ROOT}/server" "source .venv/bin/activate && python main.py"

# [3-9] Start Agent Services
echo -e "${GREEN}[3/9] Summarizer Agent (Port 8001) - Claude-powered ✨${NC}"
start_service "summarizer" 8001 "${PROJECT_ROOT}/server/services/summarizer" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

echo -e "${GREEN}[4/9] Translator Agent (Port 8002) - Claude-powered ✨${NC}"
start_service "translator" 8002 "${PROJECT_ROOT}/server/services/translator" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

echo -e "${GREEN}[5/9] Search Agent (Port 8003) - Claude-powered ✨${NC}"
start_service "search" 8003 "${PROJECT_ROOT}/server/services/search" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

echo -e "${GREEN}[6/9] Mock Busy Agent (Port 8004)${NC}"
start_service "mock_busy" 8004 "${PROJECT_ROOT}/server/services/mock_busy" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

echo -e "${GREEN}[7/9] Mock High Price Agent (Port 8005)${NC}"
start_service "mock_highprice" 8005 "${PROJECT_ROOT}/server/services/mock_highprice" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

echo -e "${GREEN}[8/9] Mock Negotiator Agent (Port 8006)${NC}"
start_service "mock_negotiator" 8006 "${PROJECT_ROOT}/server/services/mock_negotiator" "source ${PROJECT_ROOT}/server/.venv/bin/activate && python app.py"

# Wait for all services to start
sleep 3

echo ""
echo "✅ All services started successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 SERVICE STATUS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  🌐 FRONTEND & BACKEND:"
echo "  • Frontend (UI):      http://localhost:5173"
echo "  • Backend API:        http://localhost:8000"
echo "  • API Docs:           http://localhost:8000/docs"
echo ""
echo "  🤖 REAL AGENTS (Claude-powered):"
echo "  • Summarizer:         http://localhost:8001 ✨"
echo "  • Translator:         http://localhost:8002 ✨"
echo "  • Search:             http://localhost:8003 ✨"
echo ""
echo "  🧪 MOCK AGENTS (Test scenarios):"
echo "  • Mock Busy:          http://localhost:8004"
echo "  • Mock High Price:    http://localhost:8005"
echo "  • Mock Negotiator:    http://localhost:8006"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Logs:              ./logs/"
echo "🛑 Stop all:          ./stop_all_services.sh"
echo ""
echo "🧪 Quick Tests:"
echo "  # Health check"
echo "  curl http://localhost:8000/health"
echo "  curl http://localhost:8001/health"
echo ""
echo "  # Test agent"
echo "  curl -X POST http://localhost:8001/execute \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"text\":\"AI is transforming technology.\"}'"
echo ""
echo "Happy hacking! 🚀"
echo ""
