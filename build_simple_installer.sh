#!/bin/bash

# Simple installer - creates a portable folder with all files
# No compilation needed, just copy and run

APP_NAME="aiD_PM_Portable"
VERSION="1.0.0"
OUTPUT_DIR="dist/${APP_NAME}_v${VERSION}"

echo "=========================================="
echo "  Creating Portable Installation"
echo "=========================================="
echo ""

# Clean previous builds
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Copy application files
echo "📦 Copying application files..."
cp -R templates "$OUTPUT_DIR/"
cp -R templates_excel "$OUTPUT_DIR/"
cp *.py "$OUTPUT_DIR/" 2>/dev/null || true
cp requirements.txt "$OUTPUT_DIR/"

# Copy or create database
if [ -f "pm_system.db" ]; then
    echo "📊 Copying existing database..."
    cp pm_system.db "$OUTPUT_DIR/"
fi

# Create virtual environment in the package
echo "🐍 Creating virtual environment..."
cd "$OUTPUT_DIR"
python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create launcher script
echo "📝 Creating launcher..."
cat > run.sh << 'EOF'
#!/bin/bash

# aiD_PM Portable Launcher

cd "$(dirname "$0")"

echo "=========================================="
echo "  aiD Project Management System"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Initialize database if needed
if [ ! -f "pm_system.db" ]; then
    echo "🔧 Initializing database..."
    python init_db.py
fi

# Start server
echo "✅ Starting server..."
echo ""
echo "🌐 Open your browser to: http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Open browser after delay
(sleep 2 && open http://127.0.0.1:8000) &

# Start uvicorn
uvicorn main:app --host 127.0.0.1 --port 8000
EOF

chmod +x run.sh

# Create stop script
cat > stop.sh << 'EOF'
#!/bin/bash
echo "Stopping server..."
pkill -f "uvicorn main:app"
echo "Server stopped"
EOF

chmod +x stop.sh

# Create README
cat > README.txt << EOF
aiD Project Management System v$VERSION
Portable Edition
========================================

QUICK START:
1. Double-click "run.sh" or run: ./run.sh
2. Your browser will open automatically
3. Press Ctrl+C in the terminal to stop

REQUIREMENTS:
- macOS 10.14 or later
- Python 3.8 or later (included in macOS)

FEATURES:
✓ No installation needed
✓ All data stored in this folder
✓ Fully portable - can run from USB drive
✓ Multiple instances supported (different folders)

FILES:
- run.sh          : Start the application
- stop.sh         : Stop the server
- pm_system.db    : Database (created on first run)
- exports/        : PDF and Excel exports
- backups_auto/   : Automatic backups

MOVING/COPYING:
You can copy this entire folder to any location or computer.
All your data travels with the application.

UNINSTALL:
Simply delete this folder. No system files are modified.

SUPPORT:
For issues, check the logs in the terminal window.
EOF

cd ..

# Create ZIP archive
echo "🗜️  Creating ZIP archive..."
zip -q -r "${APP_NAME}_v${VERSION}.zip" "${APP_NAME}_v${VERSION}"

echo ""
echo "✅ Portable installation created!"
echo ""
echo "📦 Location: $OUTPUT_DIR"
echo "📦 ZIP file: dist/${APP_NAME}_v${VERSION}.zip"
echo "📏 Size: $(du -sh "$OUTPUT_DIR" | cut -f1)"
echo ""
echo "To test locally:"
echo "  cd '$OUTPUT_DIR'"
echo "  ./run.sh"
echo ""
echo "To distribute:"
echo "  Share the ZIP file: ${APP_NAME}_v${VERSION}.zip"
echo "  Users just unzip and run ./run.sh"
echo ""
