#!/bin/bash

# Stop the background server

cd "$(dirname "$0")"

if [ ! -f "server.pid" ]; then
    echo "❌ No server PID file found"
    echo "   Server may not be running"
    exit 1
fi

PID=$(cat server.pid)

if ps -p $PID > /dev/null 2>&1; then
    echo "Stopping server (PID: $PID)..."
    kill $PID
    rm server.pid
    echo "✅ Server stopped"
else
    echo "⚠️  Server is not running (PID $PID not found)"
    rm server.pid
fi
