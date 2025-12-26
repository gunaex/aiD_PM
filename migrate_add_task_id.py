#!/usr/bin/env python3
"""
Migration script to add task_id field to existing tasks
Run this script once to update the database schema and generate Task IDs for existing tasks
"""

import re
from sqlalchemy import text
from database import engine, get_db
import models

def migrate_add_task_id():
    """Add task_id column and generate IDs for existing tasks"""
    
    with engine.connect() as connection:
        print("Starting Task ID migration...")
        
        # Step 1: Add the task_id column (nullable first)
        try:
            connection.execute(text("ALTER TABLE tasks ADD COLUMN task_id TEXT"))
            connection.commit()
            print("✅ Added task_id column")
        except Exception as e:
            if "duplicate column name" in str(e).lower():
                print("ℹ️  task_id column already exists")
            else:
                print(f"❌ Error adding column: {e}")
                return False
        
        # Step 2: Generate Task IDs for existing tasks
        db = next(get_db())
        tasks_without_id = db.query(models.Task).filter(models.Task.task_id.is_(None)).all()
        
        print(f"Found {len(tasks_without_id)} tasks without Task ID")
        
        for task in tasks_without_id:
            project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
            if project:
                # Generate Task ID
                customer_clean = re.sub(r'[^A-Za-z0-9]', '', project.customer or 'GEN')[:3].upper().ljust(3, 'X')
                project_clean = re.sub(r'[^A-Za-z0-9]', '', project.name or 'PRJ')[:3].upper().ljust(3, 'X')
                base_prefix = f"{customer_clean}{project_clean}"
                
                # Find next available number for this specific prefix
                existing_tasks = db.query(models.Task).filter(
                    models.Task.task_id.like(f"{base_prefix}%"),
                    models.Task.task_id.isnot(None)
                ).all()
                
                # Get existing numbers for this prefix
                used_numbers = []
                for existing_task in existing_tasks:
                    if len(existing_task.task_id) >= 6 and existing_task.task_id.startswith(base_prefix):
                        try:
                            num = int(existing_task.task_id[-3:])
                            used_numbers.append(num)
                        except ValueError:
                            continue
                
                # Find the next available number
                next_number = 1
                while next_number in used_numbers:
                    next_number += 1
                
                task_id = f"{base_prefix}{next_number:03d}"
                
                # Update task
                task.task_id = task_id
                print(f"   Generated ID: {task_id} for task '{task.task_name}'")
                
                # Commit each task to avoid constraint issues
                db.commit()
        print(f"✅ Generated Task IDs for {len(tasks_without_id)} tasks")
        
        # Step 3: Make task_id column NOT NULL and UNIQUE
        try:
            connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_tasks_task_id ON tasks(task_id)"))
            connection.commit()
            print("✅ Added unique index on task_id")
        except Exception as e:
            print(f"⚠️  Warning creating unique index: {e}")
        
        print("🎉 Task ID migration completed successfully!")
        return True

if __name__ == "__main__":
    migrate_add_task_id()