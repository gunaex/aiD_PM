import os
import re

# Directory containing templates
TEMPLATES_DIR = r"d:/git/aiD_PM/templates"

# The new sidebar navigation structure
NEW_NAV_CONTENT = """            <nav class="flex-1 mt-4 overflow-y-auto">
                <a href="/"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Dashboard</a>
                <a href="/projects/list"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Projects</a>
                <a href="/kanban"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Kanban</a>
                <a href="/gantt"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Gantt</a>
                <a href="/calendar-grid"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Calendar</a>
                
                <div class="px-6 py-2 mt-4 text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Management Control
                </div>
                <a href="/resources"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Resources</a>
                <a href="/workload"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Workload</a>
                <a href="/phases"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Phases</a>
                <a href="/issues"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">Issues</a>
                <a href="/ai-assistant"
                    class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition">AI Assistant</a>
            </nav>"""

def update_sidebar(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the nav section
    # Looking for <nav ...> ... </nav>
    # We'll try to match the existing structure loosely to replace it
    pattern = re.compile(r'<nav class="flex-1 mt-4 overflow-y-auto">.*?</nav>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(NEW_NAV_CONTENT, content)
        
        # Restore active state logic (simple heuristic)
        # If the file corresponds to a link, add 'sidebar-item-active' and 'text-white'
        filename = os.path.basename(file_path)
        
        active_map = {
            'dashboard.html': 'href="/"',
            'projects.html': 'href="/projects/list"',
            'kanban.html': 'href="/kanban"',
            'gantt.html': 'href="/gantt"',
            'calendar.html': 'href="/calendar-grid"',
            'calendar_new.html': 'href="/calendar-grid"', # Assuming this is the one
            'resources.html': 'href="/resources"',
            'workload.html': 'href="/workload"',
            'phases.html': 'href="/phases"',
            'issues.html': 'href="/issues"',
            'ai_assistant.html': 'href="/ai-assistant"',
            'create_project.html': 'href="/projects/list"', # Parent
            'project_details.html': 'href="/projects/list"', # Parent
            'create_task.html': 'href="/projects/list"', # Parent
            'edit_task.html': 'href="/projects/list"', # Parent
            'issue_details.html': 'href="/issues"', # Parent
            'create_issue.html': 'href="/issues"', # Parent
            'project_history.html': 'href="/projects/list"', # Parent
            'admin_tasks.html': 'href="/projects/list"', # Parent
            'daily_tracking.html': 'href="/projects/list"', # Parent
            'settings.html': 'href="/"', # Default
        }
        
        target_href = active_map.get(filename)
        if target_href:
            # Remove existing active classes first to be clean
            new_content = new_content.replace('sidebar-item-active text-white', '')
            
            # Add active class to the target link
            # We look for the specific href and append the class
            replacement = f'{target_href}\n                    class="flex items-center px-6 py-3 sidebar-item-active text-white hover:bg-slate-900 hover:text-white transition"'
            
            # We need to be careful not to replace it if it's already there (though we just removed it from the template string, 
            # but the template string doesn't have it).
            # The template string uses a standard class string.
            standard_class = 'class="flex items-center px-6 py-3 hover:bg-slate-900 hover:text-white transition"'
            
            # Find the specific link and replace its class
            link_pattern = f'{target_href}\n                    {standard_class}'
            new_content = new_content.replace(link_pattern, replacement)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"Skipped {os.path.basename(file_path)} (nav not found)")

def main():
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".html"):
            update_sidebar(os.path.join(TEMPLATES_DIR, filename))

if __name__ == "__main__":
    main()
