#!/bin/bash

# Build macOS Application Bundle for aiD_PM
# Creates a standalone .app that can be distributed

set -e

APP_NAME="aiD_PM"
VERSION="1.0.0"
BUILD_DIR="build"
DIST_DIR="dist"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"

echo "=========================================="
echo "  Building $APP_NAME v$VERSION for macOS"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Install PyInstaller if not present
echo "📦 Checking dependencies..."
pip install -q pyinstaller pillow 2>/dev/null || true

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR" *.spec

# Create standalone launcher script
echo "📝 Creating launcher..."
cat > launcher.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import time

def main():
    # Get the application directory
    if getattr(sys, 'frozen', False):
        app_dir = os.path.dirname(sys.executable)
    else:
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(app_dir)
    
    # Check if database exists, create if not
    db_path = os.path.join(app_dir, "pm_system.db")
    if not os.path.exists(db_path):
        print("Initializing database...")
        try:
            import init_db
        except:
            pass
    
    # Start the server
    print("=" * 50)
    print("  aiD Project Management System")
    print("  Starting server...")
    print("=" * 50)
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start uvicorn
    os.system('uvicorn main:app --host 127.0.0.1 --port 8000')

if __name__ == '__main__':
    main()
EOF

# Create PyInstaller spec file
echo "⚙️  Creating PyInstaller configuration..."
cat > aiD_PM.spec << EOF
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('templates_excel', 'templates_excel'),
        ('pm_system.db', '.'),
        ('*.py', '.'),
    ],
    hiddenimports=[
        'uvicorn',
        'fastapi',
        'jinja2',
        'sqlalchemy',
        'fpdf',
        'openpyxl',
        'starlette',
        'pydantic',
        'multipart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='$APP_NAME',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='$APP_NAME',
)

app = BUNDLE(
    coll,
    name='$APP_NAME.app',
    icon=None,
    bundle_identifier='com.aid.pm',
    version='$VERSION',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '$VERSION',
    },
)
EOF

# Build the application
echo "🔨 Building application (this may take a few minutes)..."
pyinstaller --clean --noconfirm aiD_PM.spec

# Check if build succeeded
if [ -d "$APP_BUNDLE" ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📦 Application created at: $APP_BUNDLE"
    echo "📏 Size: $(du -sh "$APP_BUNDLE" | cut -f1)"
    echo ""
    echo "To run the app:"
    echo "  open $APP_BUNDLE"
    echo ""
    echo "To create a DMG installer:"
    echo "  ./create_dmg.sh"
    echo ""
else
    echo "❌ Build failed!"
    exit 1
fi
