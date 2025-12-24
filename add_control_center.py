import os
import re

# Directory containing HTML templates
templates_dir = "templates"

# Pattern to find the Management Control section
pattern = r'(<div class="px-6 py-2 mt-4 text-xs font-bold text-slate-500 uppercase tracking-wider">\s*Management Control\s*</div>)'

# Replacement text - add Control Center link right after the header
replacement = r'''\1
                <a href="/management-control"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Control Center</a>'''

# Process all HTML files
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if Management Control section exists and Control Center link doesn't
        if 'Management Control' in content and 'Control Center' not in content:
            # Add Control Center link
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Updated {filename}")
            else:
                print(f"- Skipped {filename} (pattern not matched)")
        else:
            print(f"- Skipped {filename} (already has Control Center or no Management Control section)")

print("\nSidebar update completed!")
