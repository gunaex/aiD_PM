#!/usr/bin/env python3
"""
Fix duplicate Task IDs
"""

import re
from database import get_db
import models

def fix_duplicate_task_ids():
    """Fix duplicate Task IDs by regenerating them"""
    
    db = next(get_db())
    
    # Get all tasks grouped by Task ID to find duplicates
    all_tasks = db.query(models.Task).all()
    task_id_groups = {}
    
    for task in all_tasks:
        if task.task_id:
            if task.task_id not in task_id_groups:
                task_id_groups[task.task_id] = []
            task_id_groups[task.task_id].append(task)
    
    # Find and fix duplicates
    duplicates_found = 0
    for task_id, tasks in task_id_groups.items():
        if len(tasks) > 1:
            print(f"Found {len(tasks)} tasks with duplicate ID: {task_id}")
            duplicates_found += 1
            
            # Keep the first task with original ID, reassign others
            for i, task in enumerate(tasks[1:], 2):
                project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
                if project:
                    customer_clean = re.sub(r'[^A-Za-z0-9]', '', project.customer or 'GEN')[:3].upper().ljust(3, 'X')
                    project_clean = re.sub(r'[^A-Za-z0-9]', '', project.name or 'PRJ')[:3].upper().ljust(3, 'X')
                    base_prefix = f"{customer_clean}{project_clean}"
                    
                    # Find next available number
                    existing_tasks = db.query(models.Task).all()
                    used_numbers = []
                    for existing_task in existing_tasks:
                        if (existing_task.task_id and 
                            len(existing_task.task_id) >= 6 and 
                            existing_task.task_id.startswith(base_prefix)):
                            try:
                                num = int(existing_task.task_id[-3:])
                                used_numbers.append(num)
                            except ValueError:
                                continue
                    
                    # Find next available number
                    next_number = 1
                    while next_number in used_numbers:
                        next_number += 1
                    
                    new_task_id = f"{base_prefix}{next_number:03d}"
                    task.task_id = new_task_id
                    print(f"   Reassigned: {task.task_name} -> {new_task_id}")
                    
                    # Update used numbers for next iteration
                    used_numbers.append(next_number)
    
    if duplicates_found > 0:
        db.commit()
        print(f"✅ Fixed {duplicates_found} duplicate Task ID groups")
    else:
        print("✅ No duplicate Task IDs found")

if __name__ == "__main__":
    fix_duplicate_task_ids()