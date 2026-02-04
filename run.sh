#!/bin/bash

# Change to the script's directory
cd "$(dirname "$0")"

echo "=========================================="
echo "     aiD_PM System - Server Start"
echo "=========================================="
echo ""

if [ -d ".venv" ]; then
    echo "[INFO] Activating virtual environment..."
    source .venv/bin/activate
else
    echo "[WARNING] .venv not found. Using global python..."
fi

echo "[INFO] Starting server..."
echo "[INFO] Access the dashboard at: http://localhost:8000"
echo ""

python main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Server stopped with an error."
    read -p "Press any key to continue..."
fi
