@echo off
cd /d %~dp0

echo ==========================================
echo      aiD_PM System - Server Start
echo ==========================================
echo.

if exist .venv\Scripts\activate (
    echo [INFO] Activating virtual environment...
    call .venv\Scripts\activate
) else (
    echo [WARNING] .venv not found. Using global python...
)

echo [INFO] Starting server...
echo [INFO] Access the dashboard at: http://localhost:8000
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server stopped with an error.
    pause
)
