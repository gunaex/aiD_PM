# Production Deployment Guide for macOS

## Quick Start

### Option 1: Run in Terminal (Recommended for Development)
```bash
./start_production.sh
```
- Server runs in current terminal
- Press Ctrl+C to stop
- See logs in real-time

### Option 2: Run in Background
```bash
./start_production_background.sh
```
- Server runs in background
- Logs saved to `server.log`
- Use `./stop_production.sh` to stop

### Option 3: Auto-start on Login (Optional)
Create a Launch Agent to auto-start the server when you log in:

```bash
./create_launch_agent.sh
```

## Accessing the Application

Once started, open your browser:
- **Main URL**: http://127.0.0.1:8000
- **Dashboard**: http://127.0.0.1:8000/
- **Projects**: http://127.0.0.1:8000/projects

## Managing the Server

### Check if Server is Running
```bash
ps aux | grep uvicorn
```

### View Logs (Background Mode)
```bash
tail -f server.log
```

### Stop Server (Background Mode)
```bash
./stop_production.sh
```

### Restart Server
```bash
./stop_production.sh && ./start_production_background.sh
```

## File Locations

- **Database**: `pm_system.db`
- **Exports**: `exports/`
- **Backups**: `backups_auto/`
- **Logs**: `server.log` (background mode only)

## Troubleshooting

### Port Already in Use
If port 8000 is already taken, edit the startup script and change the port:
```bash
--port 8001
```

### Database Issues
To reset the database:
```bash
python init_db.py
```

### Dependencies Missing
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Security Notes

⚠️ **Current Configuration**: Server binds to `0.0.0.0` which makes it accessible on your local network.

To restrict to localhost only, edit the startup scripts and change:
- From: `--host 0.0.0.0`
- To: `--host 127.0.0.1`

## Performance

Current setup uses 1 worker process. For better performance on multi-core systems:
- Edit startup script
- Change `--workers 1` to `--workers 2` (or 4)
