#!/bin/bash

# Create a DMG installer for macOS distribution

APP_NAME="aiD_PM"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}_v${VERSION}_macOS"
APP_BUNDLE="dist/$APP_NAME.app"
DMG_DIR="dmg_temp"
DMG_FILE="dist/${DMG_NAME}.dmg"

echo "=========================================="
echo "  Creating DMG Installer"
echo "=========================================="
echo ""

# Check if app exists
if [ ! -d "$APP_BUNDLE" ]; then
    echo "❌ Application not found at $APP_BUNDLE"
    echo "Please run ./build_macos_app.sh first"
    exit 1
fi

# Clean previous DMG
rm -rf "$DMG_DIR" "$DMG_FILE"

# Create temporary directory
echo "📁 Preparing DMG contents..."
mkdir -p "$DMG_DIR"

# Copy app to temp directory
cp -R "$APP_BUNDLE" "$DMG_DIR/"

# Create Applications symlink
ln -s /Applications "$DMG_DIR/Applications"

# Create README
cat > "$DMG_DIR/README.txt" << EOF
aiD Project Management System v$VERSION
========================================

INSTALLATION:
1. Drag aiD_PM.app to the Applications folder
2. Open aiD_PM from Applications
3. The app will start a local server and open in your browser

FIRST RUN:
- The app will create a database automatically
- Your browser will open to http://127.0.0.1:8000
- Use the system to manage projects, tasks, and resources

UNINSTALLATION:
- Simply delete aiD_PM.app from Applications

SUPPORT:
- Data is stored in: ~/Library/Application Support/aiD_PM/
- Exports are saved to: ~/Downloads/

For more information, visit the project repository.
EOF

# Create DMG
echo "💿 Creating DMG file..."
hdiutil create -volname "$APP_NAME" \
    -srcfolder "$DMG_DIR" \
    -ov -format UDZO \
    "$DMG_FILE"

# Clean up
rm -rf "$DMG_DIR"

if [ -f "$DMG_FILE" ]; then
    echo ""
    echo "✅ DMG created successfully!"
    echo ""
    echo "📦 Installer: $DMG_FILE"
    echo "📏 Size: $(du -sh "$DMG_FILE" | cut -f1)"
    echo ""
    echo "You can now distribute this DMG file."
    echo "Users can drag the app to Applications folder to install."
    echo ""
else
    echo "❌ DMG creation failed!"
    exit 1
fi
