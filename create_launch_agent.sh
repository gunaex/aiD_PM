#!/bin/bash

# Create macOS Launch Agent for auto-start on login

PLIST_FILE="$HOME/Library/LaunchAgents/com.aid.pm.plist"
CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Creating Launch Agent for aiD_PM..."
echo "Installation directory: $CURRENT_DIR"

# Create the plist file
cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aid.pm</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>cd '$CURRENT_DIR' && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>$CURRENT_DIR/launch_agent.log</string>
    
    <key>StandardErrorPath</key>
    <string>$CURRENT_DIR/launch_agent_error.log</string>
    
    <key>WorkingDirectory</key>
    <string>$CURRENT_DIR</string>
</dict>
</plist>
EOF

echo "✅ Launch Agent created: $PLIST_FILE"
echo ""
echo "To enable auto-start on login:"
echo "  launchctl load $PLIST_FILE"
echo ""
echo "To start now:"
echo "  launchctl start com.aid.pm"
echo ""
echo "To stop:"
echo "  launchctl stop com.aid.pm"
echo ""
echo "To disable auto-start:"
echo "  launchctl unload $PLIST_FILE"
echo ""
echo "Logs will be saved to:"
echo "  - $CURRENT_DIR/launch_agent.log"
echo "  - $CURRENT_DIR/launch_agent_error.log"
