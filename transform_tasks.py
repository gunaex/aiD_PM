import re

with open("templates/tasks.html", "r") as f:
    content = f.read()

# Replace titles
content = content.replace("<title>Project Functions | aiD_PM</title>", "<title>Project Tasks | aiD_PM</title>")
content = content.replace("Project Functions/Requirements", "Project Tasks")
content = content.replace("Manage project functions, requirements, and features", "Manage project tasks and activities")
content = content.replace("+ Add Function", "+ Add Task")
content = content.replace("Import Functions CSV", "Import Tasks CSV")

# Replace variables in loops and endpoints
content = content.replace("{% for func in functions %}", "{% for task in tasks %}")
content = content.replace("{% if functions %}", "{% if tasks %}")
content = content.replace("func.", "task.")
content = content.replace("functions", "tasks")
content = content.replace("/functions", "/tasks")
content = content.replace("function_code", "task_id")
content = content.replace("function_name", "task_name")
content = content.replace("Function Name", "Task Name")
content = content.replace("Function Code", "Task ID")
content = content.replace("category", "task_type")
content = content.replace("Category", "Task Type")

# Replace the edit modal text
content = content.replace("Edit Requirement", "Edit Task")
content = content.replace("editFunction", "editTask")

with open("templates/tasks.html", "w") as f:
    f.write(content)

print("Transformation complete")
