#!/bin/bash
# Script to stop all running services
# Usage: ./stop_all_services.sh

# Get absolute path of project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🛑 Stopping Agentic Marketplace Services..."
echo ""

# Function to stop a service
stop_service() {
    local name=$1
    local pidfile="${PROJECT_ROOT}/logs/${name}.pid"

    if [ -f "$pidfile" ]; then
        pid=$(cat "$pidfile")
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping $name (PID: $pid)..."
            kill $pid
            rm "$pidfile"
        else
            echo "$name is not running (stale PID file removed)"
            rm "$pidfile"
        fi
    else
        echo "$name PID file not found (may not be running)"
    fi
}

# Stop all services
stop_service "summarizer"
stop_service "translator"
stop_service "search"
stop_service "mock_busy"
stop_service "mock_highprice"
stop_service "mock_negotiator"

# Also try to kill by port (backup method)
echo ""
echo "Checking for any remaining processes on ports 8000-8006..."
for port in {8000..8006}; do
    pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo "Killing process on port $port (PID: $pid)"
        kill $pid 2>/dev/null || true
    fi
done

echo ""
echo "✅ All services stopped!"

