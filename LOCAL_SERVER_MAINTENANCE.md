# LOCAL SERVER MAINTENANCE MANUAL
**aiD_PM — AI-Powered Project Management System**
_Last updated: March 23, 2026_

---

## Table of Contents
1. [System Requirements](#1-system-requirements)
2. [First-Time Setup](#2-first-time-setup)
3. [Starting the Server](#3-starting-the-server)
4. [Stopping the Server](#4-stopping-the-server)
5. [Restarting the Server](#5-restarting-the-server)
6. [Running in Background Mode](#6-running-in-background-mode)
7. [Checking Server Status](#7-checking-server-status)
8. [Logs](#8-logs)
9. [Database Maintenance](#9-database-maintenance)
10. [Troubleshooting](#10-troubleshooting)
11. [Port Reference](#11-port-reference)

---

## 1. System Requirements

| Item | Requirement |
|------|-------------|
| OS | macOS (tested on macOS with Apple Silicon / Intel) |
| Python | 3.13+ |
| Key packages | fastapi, uvicorn, sqlalchemy, openpyxl, pandas, jinja2 |
| Database | SQLite (`pm_system.db`) — no external DB needed |
| Port | 8000 (default) |

---

## 2. First-Time Setup

Run this **once** before starting the server for the first time.

```bash
# Navigate to the project folder
cd /Users/gunaex/git_m5/aiD_PM

# Create virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Initialize the database (if pm_system.db does not exist)
python init_db.py
```

> ⚠️ **Important:** Without a `.venv`, the `uvicorn` command will not be found.
> Always activate the virtual environment before running the server.

---

## 3. Starting the Server

### Option A — Recommended: Use the startup script
```bash
cd /Users/gunaex/git_m5/aiD_PM
./run.sh
```
This auto-activates `.venv` (if present) and starts the server.

### Option B — Production mode (foreground, with logging)
```bash
cd /Users/gunaex/git_m5/aiD_PM
./start_production.sh
```

### Option C — Manual start (activate venv first)
```bash
cd /Users/gunaex/git_m5/aiD_PM
source .venv/bin/activate
python main.py
```

### Option D — Using uvicorn directly (activate venv first)
```bash
cd /Users/gunaex/git_m5/aiD_PM
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
> The `--reload` flag auto-restarts the server when code files change (use for development only).

---

## 4. Stopping the Server

### If running in foreground (Options A, B, C, D above)
```
Press Ctrl+C in the terminal
```

### If running in background
```bash
cd /Users/gunaex/git_m5/aiD_PM
./stop_production.sh
```

### Force stop by process name
```bash
pkill -f "uvicorn main:app"
```

### Force stop by port (if port 8000 is stuck)
```bash
# Find the process using port 8000
lsof -ti :8000

# Kill it
kill -9 $(lsof -ti :8000)
```

---

## 5. Restarting the Server

### Standard restart (background mode)
```bash
cd /Users/gunaex/git_m5/aiD_PM

# Step 1 — Stop
./stop_production.sh

# Step 2 — Start again in background
./start_production_background.sh
```

### Quick restart (foreground, one-liner)
```bash
cd /Users/gunaex/git_m5/aiD_PM
pkill -f "uvicorn main:app" 2>/dev/null; sleep 1; source .venv/bin/activate && python main.py
```

### Restart after code changes
```bash
cd /Users/gunaex/git_m5/aiD_PM
pkill -f "uvicorn main:app" 2>/dev/null
sleep 1
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 6. Running in Background Mode

Run the server as a background process so it keeps running after you close the terminal.

### Start in background
```bash
cd /Users/gunaex/git_m5/aiD_PM
./start_production_background.sh
```
- PID is saved to `server.pid`
- Logs are written to `server.log`

### Stop background server
```bash
./stop_production.sh
```

### View live logs (background mode)
```bash
tail -f server.log
```

### Manual nohup start (if script not available)
```bash
source .venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 > server.log 2>&1 &
echo $! > server.pid
echo "Server PID: $(cat server.pid)"
```

---

## 7. Checking Server Status

### Is the server running?
```bash
# Check by process name
ps aux | grep "uvicorn main:app"

# Check by port
lsof -i :8000

# Quick check
curl -s http://127.0.0.1:8000/ | head -5
```

### Check saved PID (background mode)
```bash
cat server.pid
ps -p $(cat server.pid)
```

### Open the web interface
Once the server is running, open a browser and go to:

| Page | URL |
|------|-----|
| Dashboard | http://127.0.0.1:8000/ |
| Projects | http://127.0.0.1:8000/projects/list |
| Phases | http://127.0.0.1:8000/phases |
| Kanban | http://127.0.0.1:8000/kanban |
| Calendar | http://127.0.0.1:8000/calendar-grid |
| Issues | http://127.0.0.1:8000/issues |
| Control Center | http://127.0.0.1:8000/management-control |
| AI Assistant | http://127.0.0.1:8000/ai-assistant |
| Settings | http://127.0.0.1:8000/settings |

---

## 8. Logs

| Log file | Description |
|----------|-------------|
| `server.log` | Output from background server (`./start_production_background.sh`) |
| Terminal output | Visible when running in foreground mode |

```bash
# Stream live logs (background mode)
tail -f server.log

# Last 100 lines
tail -100 server.log

# Search logs for errors
grep -i "error\|exception\|traceback" server.log
```

---

## 9. Database Maintenance

The app uses **SQLite** stored in `pm_system.db` in the project folder.

### Backup the database
```bash
cp pm_system.db pm_system_backup_$(date +%Y%m%d_%H%M%S).db
```

### Restore from backup
```bash
# Stop the server first!
./stop_production.sh
cp pm_system_backup_YYYYMMDD_HHMMSS.db pm_system.db
./start_production_background.sh
```

### Re-initialize database (⚠️ deletes all data)
```bash
# Only use this if the database is corrupted
source .venv/bin/activate
python init_db.py
```

### Run migrations (when new fields are added)
```bash
source .venv/bin/activate
python migrate_add_task_id.py
python migrate_resources.py
# (run any migrate_*.py scripts as needed)
```

---

## 10. Troubleshooting

### `uvicorn: command not found` or `source: no such file or directory: .venv/bin/activate`
The virtual environment does not exist yet (first-time setup required).
```bash
# Create venv and install all packages (run once)
cd /Users/gunaex/git_m5/aiD_PM
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Verify uvicorn installed correctly
uvicorn --version
# Expected: Running uvicorn 0.40.0 with CPython 3.13.x on Darwin
```
> After this, always activate first: `source .venv/bin/activate`

### Port 8000 already in use
```bash
# Find what is using it
lsof -i :8000

# Kill the process
kill -9 $(lsof -ti :8000)
```

### Server starts but browser shows nothing / 500 error
```bash
# Check logs for Python errors
tail -50 server.log

# Or run in foreground to see errors live
source .venv/bin/activate
python main.py
```

### Database locked or corrupted
```bash
# Stop the server
pkill -f "uvicorn main:app"

# Backup the broken db
cp pm_system.db pm_system_broken_$(date +%Y%m%d).db

# Re-init (CAUTION: data loss)
source .venv/bin/activate
python init_db.py
```

### Changes to code not reflected in browser
- If running with `--reload`, changes apply automatically.
- If running without `--reload`, restart the server.
- Also try a hard refresh in the browser: **Cmd+Shift+R** (macOS)

---

## 11. Port Reference

| Service | Host | Port | URL |
|---------|------|------|-----|
| aiD_PM Web Server | 0.0.0.0 | 8000 | http://127.0.0.1:8000 |

To change the port, edit `main.py` at the bottom:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # change port here
```
Or pass `--port` when using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 9000
```

---

_For questions or issues, refer to `README.md`, `QUICKSTART.md`, or `PRODUCTION_GUIDE.md` in the project root._
