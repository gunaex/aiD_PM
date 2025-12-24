import os
import re

# Directory containing HTML templates
templates_dir = "templates"

# Process all HTML files to add spacing before Control Center
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add a divider/spacing before Control Center for visual separation
        # Find the pattern where Control Center appears right after Calendar
        pattern = r'(Calendar</a>\s*)\n(<a href="/management-control")'
        replacement = r'\1\n                \n                <div class="px-6 py-2 mt-4 mb-2 border-t border-slate-700"></div>\n                \2'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Added spacing to {filename}")

print("\n✅ Sidebar cleanup complete!")
