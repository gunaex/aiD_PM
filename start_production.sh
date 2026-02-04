#!/bin/bash

# Production startup script for aiD_PM on macOS
# This script activates the virtual environment and starts the server

cd "$(dirname "$0")"

echo "=========================================="
echo "  aiD Project Management System"
echo "  Production Mode"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if database exists
if [ ! -f "pm_system.db" ]; then
    echo "⚠️  Database not found. Creating new database..."
    python init_db.py
fi

# Display server info
echo "✅ Starting server in production mode..."
echo ""
echo "🌐 Server will be available at:"
echo "   http://127.0.0.1:8000"
echo "   http://localhost:8000"
echo ""
echo "📊 Dashboard: http://127.0.0.1:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info
