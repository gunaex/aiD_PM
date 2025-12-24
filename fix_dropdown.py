import os

TEMPLATES_DIR = "templates"

def fix_dropdown_color():
    files = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".html")]
    
    for filename in files:
        filepath = os.path.join(TEMPLATES_DIR, filename)
        print(f"Processing {filename}...")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Target: <select id="project_filter" ... class="border border-slate-300 ...">
        # We want to add text-slate-900 to the class list
        
        # Pattern 1: class="border border-slate-300
        if 'class="border border-slate-300' in content:
            content = content.replace(
                'class="border border-slate-300', 
                'class="text-slate-900 border border-slate-300'
            )
            
        # Pattern 2: class="border border-gray-300 (just in case)
        if 'class="border border-gray-300' in content:
            content = content.replace(
                'class="border border-gray-300', 
                'class="text-slate-900 border border-gray-300'
            )
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print("All files processed.")

if __name__ == "__main__":
    fix_dropdown_color()
