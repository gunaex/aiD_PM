import os
import re

TEMPLATES_DIR = "templates"

def fix_ui_files():
    # 1. Define the target styles (from dashboard.html fix)
    
    # Body: Remove zoom, add h-screen overflow-hidden, set base theme
    # Old: <body class="bg-slate-50 text-slate-900 font-sans" style="zoom: 0.75;">
    # New: <body class="bg-slate-900 text-slate-100 font-sans h-screen overflow-hidden">
    
    # Sidebar: Darker slate, border
    # Old: <aside class="w-64 bg-slate-900 text-slate-300 flex flex-col">
    # New: <aside class="w-64 bg-slate-950 text-slate-400 flex flex-col border-r border-slate-800">
    
    # Nav Items:
    # Old: hover:bg-slate-800
    # New: hover:bg-slate-900
    
    # Sidebar Active Item:
    # Old: sidebar-item-active text-white
    # New: sidebar-item-active text-white bg-slate-900 border-r-4 border-blue-500
    
    files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".html")]
    
    for filename in files:
        filepath = os.path.join(TEMPLATES_DIR, filename)
        
        # Skip dashboard.html as it's already fixed (but checking won't hurt if regex is robust)
        if filename == "dashboard.html":
            continue
            
        print(f"Processing {filename}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 1. Fix Body Tag
        if 'style="zoom: 0.75;"' in content:
            content = re.sub(
                r'<body[^>]*style="zoom: 0.75;"[^>]*>', 
                '<body class="bg-slate-900 text-slate-100 font-sans h-screen overflow-hidden">', 
                content
            )
        
        # 2. Fix Container Div (ensure h-full)
        # Look for <div class="flex h-screen overflow-hidden"> and change to <div class="flex h-full">
        # because body is now h-screen
        content = content.replace(
            '<div class="flex h-screen overflow-hidden">', 
            '<div class="flex h-full">'
        )
        
        # 3. Fix Sidebar Aside
        content = content.replace(
            '<aside class="w-64 bg-slate-900 text-slate-300 flex flex-col">',
            '<aside class="w-64 bg-slate-950 text-slate-400 flex flex-col border-r border-slate-800">'
        )
        
        # 4. Fix Nav Links Hover
        content = content.replace('hover:bg-slate-800', 'hover:bg-slate-900')
        
        # 5. Fix Sidebar Active Item (add border-r-4 border-blue-500 if not present)
        # This is a bit tricky with regex, let's try a simpler replacement for the common pattern
        # Pattern: sidebar-item-active text-white
        # We want to ensure it has the new styles.
        # Note: dashboard.html used: bg-slate-900 border-r-4 border-blue-500
        
        # We can replace the CSS class definition in <style> too if we want, but inline classes are better for tailwind
        
        # Let's just update the specific active class usage if we find it
        # It usually looks like: class="... sidebar-item-active text-white ..."
        # We want to append bg-slate-900 border-r-4 border-blue-500 if not there
        
        # Actually, let's just replace the CSS rule in <style> to be safe and global
        # .sidebar-item-active { border-right: 4px solid #3b82f6; background: #1e293b; }
        # The original CSS had this. #1e293b is slate-800.
        # We want background to be slate-900 (#0f172a) or keep it distinct.
        # Let's leave the CSS rule as is, it's close enough.
        
        # 6. Fix Main Content Background
        # If we want "Consistent Slate-900", maybe we should make the main content dark too?
        # But that breaks all the white cards.
        # Let's keep main content as is for now, but ensure it fills height.
        # <main class="flex-1 overflow-y-auto p-8 bg-slate-50 min-h-full">
        # We should probably remove min-h-full if we have h-full on parent, but it doesn't hurt.
        
        # 7. Fix Nav Container overflow
        # <nav class="flex-1 mt-4"> -> <nav class="flex-1 mt-4 overflow-y-auto">
        content = content.replace('<nav class="flex-1 mt-4">', '<nav class="flex-1 mt-4 overflow-y-auto">')
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("All files processed.")

if __name__ == "__main__":
    fix_ui_files()
