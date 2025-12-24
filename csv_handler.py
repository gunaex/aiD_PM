"""
CSV Handler for Task Import/Export
Handles bulk task operations with strict validation
"""
import csv
import io
from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
import models


def validate_date_format(date_str: str) -> Tuple[bool, str]:
    """
    Validate date string in YYYYMMDD format
    Returns: (is_valid, error_message)
    """
    if not date_str or date_str.strip() == "":
        return True, ""  # Empty dates are allowed
    
    date_str = date_str.strip()
    
    # Check format
    if len(date_str) != 8 or not date_str.isdigit():
        return False, f"Invalid date format '{date_str}', expected YYYYMMDD"
    
    # Validate actual date
    try:
        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        datetime(year, month, day)
        return True, ""
    except ValueError:
        return False, f"Invalid date '{date_str}' (date doesn't exist)"


def parse_date(date_str: str):
    """Convert YYYYMMDD string to date object"""
    if not date_str or date_str.strip() == "":
        return None
    date_str = date_str.strip()
    year = int(date_str[0:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    return datetime(year, month, day).date()


def format_date_for_export(date_obj) -> str:
    """Convert date object to YYYYMMDD string"""
    if not date_obj:
        return ""
    return date_obj.strftime("%Y%m%d")


def export_tasks_to_csv(project_id: int, db: Session) -> str:
    """
    Export all tasks for a project to CSV format
    Returns CSV string content with proper Unicode support
    """
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    
    # Write header
    writer.writerow([
        "Task ID", "Task Name", "Task Type", "Weight Score", "Phase",
        "Assigned Resources", "Planned Start", "Planned End", "Progress"
    ])
    
    # Write tasks
    for task in tasks:
        # Get phase name
        phase_name = ""
        if task.phase_id:
            phase = db.query(models.ProjectPhase).filter(models.ProjectPhase.id == task.phase_id).first()
            if phase:
                phase_name = phase.phase_name
        
        # Get assigned resources
        resource_names = []
        if task.assigned_resource_id:
            resource = db.query(models.Resource).filter(models.Resource.id == task.assigned_resource_id).first()
            if resource:
                resource_names.append(resource.full_name)
        
        # Get multi-assigned resources
        task_resources = db.query(models.TaskResource).filter(models.TaskResource.task_id == task.id).all()
        for tr in task_resources:
            resource = db.query(models.Resource).filter(models.Resource.id == tr.resource_id).first()
            if resource and resource.full_name not in resource_names:
                resource_names.append(resource.full_name)
        
        writer.writerow([
            task.id,
            task.task_name,
            task.task_type,
            task.weight_score,
            phase_name,
            ",".join(resource_names),
            format_date_for_export(task.planned_start),
            format_date_for_export(task.planned_end),
            int(task.actual_progress)
        ])
    
    return output.getvalue()


def generate_blank_template() -> str:
    """Generate blank CSV template with headers only and proper Unicode support"""
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        "Task ID", "Task Name", "Task Type", "Weight Score", "Phase",
        "Assigned Resources", "Planned Start", "Planned End", "Progress"
    ])
    return output.getvalue()


def validate_csv_file(csv_content: str, project_id: int, db: Session) -> Tuple[bool, List[str]]:
    """
    Validate entire CSV file before import with Unicode support
    Returns: (is_valid, error_messages)
    """
    errors = []
    
    try:
        # Handle potential BOM and ensure proper Unicode handling
        if csv_content.startswith('\ufeff'):
            csv_content = csv_content[1:]
        
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Check required columns
        required_columns = ["Task Name", "Planned Start", "Planned End"]
        if not all(col in reader.fieldnames for col in required_columns):
            missing = [col for col in required_columns if col not in reader.fieldnames]
            errors.append(f"Missing required columns: {', '.join(missing)}")
            return False, errors
        
        # Validate each row
        for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
            # Check mandatory fields
            if not row.get("Task Name", "").strip():
                errors.append(f"Row {row_num}: Missing Task Name")
            
            if not row.get("Planned Start", "").strip():
                errors.append(f"Row {row_num}: Missing Planned Start")
            
            if not row.get("Planned End", "").strip():
                errors.append(f"Row {row_num}: Missing Planned End")
            
            # Validate date formats
            planned_start = row.get("Planned Start", "").strip()
            if planned_start:
                is_valid, error_msg = validate_date_format(planned_start)
                if not is_valid:
                    errors.append(f"Row {row_num}: {error_msg}")
            
            planned_end = row.get("Planned End", "").strip()
            if planned_end:
                is_valid, error_msg = validate_date_format(planned_end)
                if not is_valid:
                    errors.append(f"Row {row_num}: {error_msg}")
            
            # Validate date logic (end >= start)
            if planned_start and planned_end:
                try:
                    start_date = parse_date(planned_start)
                    end_date = parse_date(planned_end)
                    if start_date and end_date and end_date < start_date:
                        errors.append(f"Row {row_num}: Planned End must be >= Planned Start")
                except:
                    pass  # Already caught by format validation
        
        return len(errors) == 0, errors
    
    except Exception as e:
        errors.append(f"CSV parsing error: {str(e)}")
        return False, errors


def import_tasks_from_csv(project_id: int, csv_content: str, db: Session) -> Dict:
    """
    Import tasks from CSV file with Unicode support
    Returns: {"success": bool, "created": int, "updated": int, "errors": []}
    """
    # Validate first
    is_valid, errors = validate_csv_file(csv_content, project_id, db)
    if not is_valid:
        return {
            "status": "error",
            "success": False,
            "created_count": 0,
            "updated_count": 0,
            "errors": errors,
            "message": "Validation failed"
        }
    
    created_count = 0
    updated_count = 0
    
    try:
        # Handle potential BOM and ensure proper Unicode handling
        if csv_content.startswith('\ufeff'):
            csv_content = csv_content[1:]
            
        reader = csv.DictReader(io.StringIO(csv_content))
        
        for row in reader:
            task_id = row.get("Task ID", "").strip()
            task_name = row.get("Task Name", "").strip()
            task_type = row.get("Task Type", "Dev").strip() or "Dev"
            weight_score = float(row.get("Weight Score", "1.0").strip() or "1.0")
            phase_name = row.get("Phase", "").strip()
            resource_names = row.get("Assigned Resources", "").strip()
            planned_start = parse_date(row.get("Planned Start", ""))
            planned_end = parse_date(row.get("Planned End", ""))
            progress = float(row.get("Progress", "0").strip() or "0")
            
            # Find phase by name
            phase_id = None
            if phase_name:
                phase = db.query(models.ProjectPhase).filter(
                    models.ProjectPhase.project_id == project_id,
                    models.ProjectPhase.phase_name == phase_name
                ).first()
                if phase:
                    phase_id = phase.id
            
            # Update or Create
            if task_id and task_id.isdigit():
                # Update existing task
                task = db.query(models.Task).filter(models.Task.id == int(task_id)).first()
                if task:
                    task.task_name = task_name
                    task.task_type = task_type
                    task.weight_score = weight_score
                    task.phase_id = phase_id
                    task.planned_start = planned_start
                    task.planned_end = planned_end
                    task.actual_progress = progress
                    updated_count += 1
                else:
                    # ID doesn't exist, create new
                    task = models.Task(
                        project_id=project_id,
                        task_name=task_name,
                        task_type=task_type,
                        weight_score=weight_score,
                        phase_id=phase_id,
                        planned_start=planned_start,
                        planned_end=planned_end,
                        actual_progress=progress
                    )
                    db.add(task)
                    created_count += 1
            else:
                # Create new task
                task = models.Task(
                    project_id=project_id,
                    task_name=task_name,
                    task_type=task_type,
                    weight_score=weight_score,
                    phase_id=phase_id,
                    planned_start=planned_start,
                    planned_end=planned_end,
                    actual_progress=progress
                )
                db.add(task)
                created_count += 1
            
            db.flush()  # Get task ID for resource assignment
            
            # Handle resource assignment (optional, skip if not found)
            if resource_names:
                names = [n.strip() for n in resource_names.split(",")]
                for name in names:
                    resource = db.query(models.Resource).filter(
                        models.Resource.full_name == name
                    ).first()
                    if resource:
                        # Check if already assigned
                        existing = db.query(models.TaskResource).filter(
                            models.TaskResource.task_id == task.id,
                            models.TaskResource.resource_id == resource.id
                        ).first()
                        if not existing:
                            task_resource = models.TaskResource(
                                task_id=task.id,
                                resource_id=resource.id
                            )
                            db.add(task_resource)
        
        db.commit()
        return {
            "status": "success",
            "success": True,
            "created_count": created_count,
            "updated_count": updated_count,
            "errors": [],
            "message": f"Successfully imported {created_count + updated_count} tasks"
        }
    
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "success": False,
            "created_count": 0,
            "updated_count": 0,
            "errors": [f"Import failed: {str(e)}"],
            "message": str(e)
        }
