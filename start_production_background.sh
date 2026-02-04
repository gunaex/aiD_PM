#!/bin/bash

# Start aiD_PM server in background mode
# Logs will be saved to server.log

cd "$(dirname "$0")"

echo "Starting aiD_PM server in background..."

# Check if server is already running
if [ -f "server.pid" ]; then
    PID=$(cat server.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo "❌ Server is already running (PID: $PID)"
        echo "   To stop it, run: ./stop_production.sh"
        exit 1
    fi
fi

# Activate virtual environment
source .venv/bin/activate

# Start server in background
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 > server.log 2>&1 &

# Save PID
echo $! > server.pid

echo "✅ Server started in background"
echo "   PID: $(cat server.pid)"
echo "   Logs: server.log"
echo "   URL: http://127.0.0.1:8000"
echo ""
echo "To stop the server, run: ./stop_production.sh"
echo "To view logs, run: tail -f server.log"
