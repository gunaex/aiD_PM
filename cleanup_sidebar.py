import os
import re

# Directory containing HTML templates
templates_dir = "templates"

# Count of files updated
updated_count = 0

# Process all HTML files
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove the "Management Control" section header
        content = re.sub(
            r'\s*<div class="px-6 py-2 mt-4 text-xs font-bold text-slate-500 uppercase tracking-wider">\s*Management Control\s*</div>\s*',
            '\n',
            content
        )
        
        # Remove Resources link
        content = re.sub(
            r'\s*<a href="/resources"[^>]*>Resources</a>\s*',
            '',
            content
        )
        
        # Remove Workload link
        content = re.sub(
            r'\s*<a href="/workload"[^>]*>Workload</a>\s*',
            '',
            content
        )
        
        # Remove AI Assistant link
        content = re.sub(
            r'\s*<a href="/ai-assistant"[^>]*>AI Assistant</a>\s*',
            '',
            content
        )
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1
            print(f"✓ Updated {filename}")
        else:
            print(f"- Skipped {filename} (no changes needed)")

print(f"\n✅ Updated {updated_count} files")
print("Sidebar now shows only Control Center under navigation!")
