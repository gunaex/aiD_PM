# macOS Installer Guide

This guide shows you how to create different types of installers for aiD_PM on macOS.

## 🎯 Choose Your Installer Type

### Option 1: Portable ZIP (Easiest & Recommended)
**Best for:** Easy distribution, no compilation, runs from any location

```bash
./build_simple_installer.sh
```

**Creates:**
- Self-contained folder with everything included
- ZIP file ready to share
- No installation needed - just unzip and run
- ~50-100 MB

**Distribution:**
- Share the ZIP file
- Users unzip and double-click `run.sh`
- Works immediately

---

### Option 2: macOS .app Bundle (Native Look)
**Best for:** Professional distribution, native macOS experience

```bash
./build_macos_app.sh
```

**Creates:**
- Native macOS .app bundle
- Can be placed in Applications folder
- ~150-200 MB

**To also create DMG installer:**
```bash
./build_macos_app.sh
./create_dmg.sh
```

**Distribution:**
- Share the DMG file
- Users open DMG, drag app to Applications
- Launches like any Mac app

---

## 📋 Step-by-Step Instructions

### Portable ZIP Installation (Recommended)

1. **Build the package:**
   ```bash
   chmod +x build_simple_installer.sh
   ./build_simple_installer.sh
   ```

2. **Test it locally:**
   ```bash
   cd dist/aiD_PM_Portable_v1.0.0
   ./run.sh
   ```

3. **Distribute:**
   - Share `dist/aiD_PM_Portable_v1.0.0.zip`
   - Users unzip anywhere
   - Double-click `run.sh` to start

### macOS App Bundle Installation

1. **Install PyInstaller:**
   ```bash
   source .venv/bin/activate
   pip install pyinstaller
   ```

2. **Build the app:**
   ```bash
   chmod +x build_macos_app.sh
   ./build_macos_app.sh
   ```
   ⏱️ Takes 3-5 minutes

3. **Test it:**
   ```bash
   open dist/aiD_PM.app
   ```

4. **Create DMG (optional):**
   ```bash
   chmod +x create_dmg.sh
   ./create_dmg.sh
   ```

5. **Distribute:**
   - Share `dist/aiD_PM_v1.0.0_macOS.dmg`
   - Users open DMG, drag to Applications
   - Launch from Applications folder

---

## 🔍 Comparison

| Feature | Portable ZIP | App Bundle + DMG |
|---------|--------------|------------------|
| Build time | ~2 minutes | ~5 minutes |
| Size | 50-100 MB | 150-200 MB |
| Installation | Unzip only | Drag to Applications |
| Updates | Replace folder | Replace app |
| Multi-instance | ✅ Easy | ❌ Harder |
| Native feel | ⚠️ Terminal | ✅ Full |
| Code signing | Not needed | Recommended |
| Gatekeeper | ⚠️ May warn | ⚠️ May warn |

---

## 🚀 Quick Commands

```bash
# Make all scripts executable
chmod +x build_*.sh create_dmg.sh

# Create portable ZIP (fastest)
./build_simple_installer.sh

# Create macOS app
./build_macos_app.sh

# Create DMG installer
./create_dmg.sh

# Clean all builds
rm -rf build dist *.spec launcher.py dmg_temp
```

---

## ⚠️ macOS Security Notes

### First-Time Launch Warning

Users may see "cannot be opened because it is from an unidentified developer."

**Solution for users:**
1. Right-click the app/file
2. Select "Open"
3. Click "Open" in the dialog
4. App will be trusted from then on

**Alternative (Terminal):**
```bash
xattr -cr /path/to/aiD_PM.app
```

### Code Signing (Advanced)

For distribution without warnings:

```bash
# Requires Apple Developer account ($99/year)
codesign --force --deep --sign "Developer ID" dist/aiD_PM.app
```

---

## 📦 What Gets Included

Both installer types include:
- All Python code (main.py, models.py, etc.)
- HTML templates
- Excel templates  
- Database (or auto-creates on first run)
- All dependencies
- Python runtime (app bundle only)

Users don't need to install anything else.

---

## 🔧 Troubleshooting

### Build fails with "PyInstaller not found"
```bash
source .venv/bin/activate
pip install pyinstaller
```

### App bundle is too large
This is normal - it includes Python runtime and all libraries.
Typical size: 150-250 MB

### Database not found error
The launcher auto-creates the database on first run.
Or copy `pm_system.db` to the dist folder before building.

### Port 8000 already in use
Edit `launcher.py` and change the port number before building.

---

## 📤 Distribution Checklist

Before sharing your installer:

- [ ] Test the installer on a clean Mac
- [ ] Verify database initializes correctly
- [ ] Check all features work (projects, tasks, exports)
- [ ] Include README with installation instructions
- [ ] Mention macOS version requirements (10.14+)
- [ ] Note the security warning workaround
- [ ] Provide support contact information

---

## 🎓 Recommendation

**For most users:** Use the **Portable ZIP** method
- Faster to build
- Smaller file size
- Easier to update
- No Gatekeeper issues
- Works from anywhere

**For professional distribution:** Use **.app + DMG**
- More professional appearance
- Integrates with macOS
- Better for App Store submission
- Recommended for commercial use
