import re

with open("templates/tasks.html", "r") as f:
    content = f.read()

# We need to replace the table body with a flat list since tasks have no parents.
# Find the start of the table block
start_table = content.find("<table class=\"w-full text-left border-collapse\">")
end_table = content.find("</table>") + 8

new_table = """<table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 text-slate-500 text-xs uppercase font-bold">
                            <tr>
                                <th class="px-6 py-4">Task ID</th>
                                <th class="px-6 py-4">Task Name</th>
                                <th class="px-6 py-4">Type</th>
                                <th class="px-6 py-4">Effort (Est/Act)</th>
                                <th class="px-6 py-4">Progress</th>
                                <th class="px-6 py-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            {% for task in tasks %}
                            <tr class="hover:bg-slate-50 transition task-row">
                                <td class="px-6 py-4 font-mono text-xs font-bold text-slate-500">
                                    {{ task.task_id }}
                                </td>
                                <td class="px-6 py-4">
                                    <div class="font-bold text-slate-800">{{ task.task_name }}</div>
                                </td>
                                <td class="px-6 py-4">
                                    <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-[10px] uppercase font-bold">{{ task.task_type }}</span>
                                </td>
                                <td class="px-6 py-4 text-xs">
                                    <span class="text-slate-700 font-bold">{{ "%.1f"|format(task.estimated_hours) }}h Est.</span><br>
                                    <span class="text-slate-400">{{ "%.1f"|format(task.actual_hours) }}h Act.</span>
                                </td>
                                <td class="px-6 py-4 w-48">
                                    <div class="flex flex-col gap-1">
                                        <div class="flex justify-between text-[10px] font-bold text-slate-500">
                                            <span>{{ task.actual_progress|round(1) }}% Complete</span>
                                        </div>
                                        <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                                            <div class="{% if task.actual_progress == 100 %}bg-green-500{% else %}bg-blue-600{% endif %} h-full transition-all duration-500"
                                                style="width: {{ task.actual_progress }}%"></div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4">
                                    <div class="flex items-center gap-2 action-btns">
                                        <a href="/tasks/{{ task.id }}/edit" class="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 rounded transition" title="Edit">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                            </svg>
                                        </a>
                                        <form action="/tasks/{{ task.id }}/delete" method="POST" onsubmit="return confirm('Delete this task?')">
                                            <button type="submit" class="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition" title="Delete">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-4v6m4-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                                </svg>
                                            </button>
                                        </form>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>"""

content = content[:start_table] + new_table + content[end_table:]

# Now replace the create modal since tasks don't have parent_function_id
start_create = content.find('<div id="createForm"')
end_create = content.find('<!-- Functions List -->')

new_create = """<div id="createForm" class="bg-white rounded-xl border border-slate-200 shadow-sm p-6 mb-6 hidden">
                <h3 class="font-bold text-slate-800 mb-4">Add New Task</h3>
                <form action="/tasks/create" method="POST" class="space-y-4">
                    <input type="hidden" name="return_url" value="/tasks">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">Project *</label>
                            <select name="project_id" required class="form-control">
                                <option value="">-- Select Project --</option>
                                {% for project in projects %}
                                <option value="{{ project.id }}" {% if selected_project_id==project.id %}selected{% endif %}>{{ project.name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">Task Type *</label>
                            <select name="task_type" class="form-control" onchange="if(this.value === 'Other') { document.getElementById('new_task_type_container').classList.remove('hidden'); } else { document.getElementById('new_task_type_container').classList.add('hidden'); }">
                                <option value="Requirement">Requirement</option>
                                <option value="Dev" selected>Dev</option>
                                <option value="Admin">Admin</option>
                                <option value="Procurement">Procurement</option>
                                <option value="Fix">Fix</option>
                                <option value="Other">Other</option>
                            </select>
                            <div id="new_task_type_container" class="mt-2 hidden">
                                <input type="text" name="new_task_type" placeholder="Enter new task type" class="form-control text-sm">
                            </div>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-4">
                        <div class="col-span-2">
                            <label class="block text-sm font-bold text-slate-700 mb-2">Task Name *</label>
                            <input type="text" name="task_name" required placeholder="e.g., Implement Login" class="form-control">
                        </div>
                        <div>
                            <label class="block text-sm font-bold text-slate-700 mb-2">Estimated Effort (Hours)</label>
                            <input type="number" name="estimated_hours" step="0.5" value="0" class="form-control">
                        </div>
                    </div>
                    <div class="flex gap-3">
                        <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition">
                            Create Task
                        </button>
                        <button type="button" onclick="toggleCreateForm()" class="bg-slate-200 hover:bg-slate-300 text-slate-700 px-4 py-2 rounded-lg font-medium transition">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
            
            <!-- Tasks List -->
            """

content = content[:start_create] + new_create + content[end_create+23:]

# Remove edit modal
start_edit = content.find('<!-- Edit Modal')
end_edit = content.find('</script>', start_edit)
if start_edit != -1:
    content = content[:start_edit] + content[end_edit-1:] # leave script tag open

with open("templates/tasks.html", "w") as f:
    f.write(content)

