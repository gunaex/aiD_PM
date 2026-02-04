# macOS Setup Guide for aiD_PM

Welcome to macOS! This guide will help you run the aiD_PM system on your Mac.

## Good News! 🎉

**No code changes are needed!** Python is cross-platform, and your code already uses `os.path` which works on both Windows and macOS.

## Quick Start

### 1. Install Python (if not already installed)

Check if Python is installed:
```bash
python3 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/) or use Homebrew:
```bash
brew install python3
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

**Option A: Using the shell script (recommended)**
```bash
./run.sh
```

**Option B: Manually**
```bash
source .venv/bin/activate
python main.py
```

## Key Differences from Windows

| Windows | macOS/Linux |
|---------|-------------|
| `run.bat` | `run.sh` |
| `.venv\Scripts\activate` | `source .venv/bin/activate` |
| `python` | `python3` (though `python` may work) |
| Backslashes `\` in paths | Forward slashes `/` in paths |

## Troubleshooting

### Permission Denied Error
If you get "Permission denied" when running `./run.sh`:
```bash
chmod +x run.sh
```

### Python Command Not Found
Try using `python3` instead of `python`:
```bash
python3 main.py
```

### Port Already in Use
If port 8000 is already in use, you can modify `main.py` to use a different port or kill the process:
```bash
lsof -ti:8000 | xargs kill -9
```

## File Paths

The Python code uses `os.path` which automatically handles path differences:
- **Windows**: `C:\Users\...` with backslashes `\`
- **macOS**: `/Users/...` with forward slashes `/`

No changes needed in your Python files! ✅

## Database Files

Your SQLite database files (`.db` files) are also cross-platform compatible and will work without modification.

## Access the Application

Once running, access the dashboard at:
```
http://localhost:8000
```

## Deactivating Virtual Environment

When you're done:
```bash
deactivate
```
