from fastapi import FastAPI, Depends, HTTPException, Form, Request, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import datetime
import os

import models
from database import engine, get_db, init_db
import excel_engine
from ai_assistant import ai_assistant

# สร้างตารางในฐานข้อมูล
init_db()

app = FastAPI(title="Smart PM Control Tower (aiD_PM)", version="1.5.0 - AI Powered")

# ตั้งค่า Templates และ Static files
templates = Jinja2Templates(directory="templates")

# Add custom Jinja2 filter for JSON parsing
import json
def fromjson_filter(value):
    """Parse JSON string to Python dict"""
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}

templates.env.filters['fromjson'] = fromjson_filter
# app.mount("/static", StaticFiles(directory="static"), name="static")  # Uncomment เมื่อมีไฟล์ static


# ==================== Pydantic Schemas ====================

class ResourceCreate(BaseModel):
    full_name: str
    nickname: Optional[str] = None
    position: Optional[str] = None
    skills: Optional[dict] = None  # {"Python": 9, "SQL": 7}
    speed_score: Optional[int] = 5
    quality_score: Optional[int] = 5

class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    full_name: str
    nickname: Optional[str]
    position: Optional[str]
    skills: Optional[dict]
    speed_score: Optional[int]
    quality_score: Optional[int]
    is_active: bool

class ProjectCreate(BaseModel):
    name: str
    customer: Optional[str] = None
    methodology: Optional[str] = "Scrum"  # Waterfall, Scrum, Kanban
    is_recovery_mode: bool = False
    budget_masked: Optional[str] = None

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    customer: Optional[str]
    methodology: Optional[str]
    is_recovery_mode: bool
    budget_masked: Optional[str]
    progress: Optional[float] = 0.0
    created_at: datetime.datetime

class TaskCreate(BaseModel):
    project_id: int
    task_name: str
    task_type: Optional[str] = "Dev"  # Dev, Admin, Procurement
    weight_score: float = 1.0
    planned_start: Optional[datetime.date] = None
    planned_end: Optional[datetime.date] = None
    assigned_resource_id: Optional[int] = None

class TaskUpdate(BaseModel):
    actual_progress: Optional[float] = None
    assigned_resource_id: Optional[int] = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    project_id: int
    task_name: str
    task_type: Optional[str]
    weight_score: float
    planned_start: Optional[datetime.date]
    planned_end: Optional[datetime.date]
    actual_progress: float
    assigned_resource_id: Optional[int]
    ai_risk_score: float

class WeeklySnapshotCreate(BaseModel):
    project_id: int
    week_number: int
    plan_acc: float
    actual_acc: float

class WeeklySnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    project_id: int
    week_number: int
    plan_acc: float
    actual_acc: float

# ==================== AI Smart Matching Logic ====================

def calculate_matching_score(resource: models.Resource, task: models.Task) -> float:
    """
    Hidden AI Intelligence: คำนวณคะแนนความเหมาะสมระหว่าง Resource กับ Task
    
    Logic:
    - ถ้า Task type ตรงกับ skill ของ Resource จะได้คะแนนสูง
    - Speed score และ Quality score มีผลต่อการคำนวณ
    - Return: Score 0-100
    """
    score = 0.0
    
    if resource.skills and task.task_type:
        # ตรวจสอบว่า Resource มี skill ที่ตรงกับ task_type หรือไม่
        task_type_lower = task.task_type.lower()
        for skill_name, skill_level in resource.skills.items():
            if task_type_lower in skill_name.lower():
                score += skill_level * 5  # skill level 1-10 -> max 50 points
    
    # เพิ่มคะแนนจาก speed และ quality
    if resource.speed_score:
        score += resource.speed_score * 2.5  # max 25 points
    if resource.quality_score:
        score += resource.quality_score * 2.5  # max 25 points
    
    return min(score, 100.0)  # จำกัดไม่เกิน 100

def suggest_best_resource(db: Session, task_id: int) -> Optional[dict]:
    """
    แนะนำ Resource ที่เหมาะสมที่สุดสำหรับ Task
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        return None
    
    active_resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    
    if not active_resources:
        return None
    
    # คำนวณคะแนนสำหรับทุก Resource
    resource_scores = []
    for resource in active_resources:
        score = calculate_matching_score(resource, task)
        resource_scores.append({
            "resource_id": resource.id,
            "full_name": resource.full_name,
            "nickname": resource.nickname,
            "score": score
        })
    
    # เรียงตามคะแนนจากมากไปน้อย
    resource_scores.sort(key=lambda x: x["score"], reverse=True)
    
    return resource_scores[0] if resource_scores else None

def get_system_recommendation(task_type: str, db: Session) -> dict:
    """
    Simple Hidden AI Logic: แนะนำคนจาก Skill และ Speed/Quality score
    """
    if task_type in ["Dev", "Fix"]:
        best_match = db.query(models.Resource).filter(models.Resource.is_active == True).order_by(models.Resource.speed_score.desc()).first()
    else:
        best_match = db.query(models.Resource).filter(models.Resource.is_active == True).order_by(models.Resource.quality_score.desc()).first()
    
    if best_match:
        return {
            "recommended_id": best_match.id,
            "nickname": best_match.nickname,
            "reason": f"System suggests {best_match.nickname} for this {task_type} task based on performance characteristics."
        }
    return {"recommended_id": None, "nickname": None, "reason": "No recommendation available."}

# ==================== HTML Pages ====================

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """หน้า Dashboard หลัก (Control Tower) - แสดงข้อมูลจริง"""
    projects = db.query(models.Project).all()
    
    # ดึงงานที่เป็น Blocker/Admin มาโชว์ในหน้าแรก
    pending_admin_tasks = db.query(models.Task).filter(
        models.Task.task_type.in_(['Admin', 'Procurement', 'PR', 'PO']),
        models.Task.actual_progress < 100
    ).all()
    
    # คำนวณ Progress จริงสำหรับแต่ละโปรเจกต์ (Value-Based)
    projects_with_progress = []
    for project in projects:
        tasks = db.query(models.Task).filter(models.Task.project_id == project.id).all()
        
        if tasks:
            total_weight = sum(t.weight_score for t in tasks)
            weighted_progress = sum((t.actual_progress / 100) * t.weight_score for t in tasks)
            progress = (weighted_progress / total_weight * 100) if total_weight > 0 else 0
        else:
            progress = 0
        
        projects_with_progress.append({
            'project': project,
            'progress': round(progress, 1),
            'task_count': len(tasks),
            'completed_tasks': len([t for t in tasks if t.actual_progress == 100])
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "projects_with_progress": projects_with_progress,
        "admin_tasks": pending_admin_tasks,
        "current_date": datetime.date.today().strftime("%d %b %Y")
    })

@app.get("/api/resources/{resource_id}")
def get_resource_detail(resource_id: int, db: Session = Depends(get_db)):
    """Get detailed resource information for editing"""
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {
        "id": resource.id,
        "full_name": resource.full_name,
        "nickname": resource.nickname or "",
        "position": resource.position or "",
        "company": resource.company or "",
        "skills": resource.skills or "",
        "is_active": resource.is_active
    }

@app.put("/api/resources/{resource_id}")
def update_resource(
    resource_id: int,
    full_name: str = Form(...),
    nickname: str = Form(...),
    position: str = Form(...),
    company: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    is_active: bool = Form(True),
    db: Session = Depends(get_db)
):
    """Update resource information"""
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.full_name = full_name
    resource.nickname = nickname
    resource.position = position
    resource.company = company
    resource.skills = skills
    resource.is_active = is_active
    
    db.commit()
    db.refresh(resource)
    
    return {"success": True, "message": "Resource updated successfully"}

@app.patch("/api/resources/{resource_id}/toggle-status")
def toggle_resource_status(resource_id: int, db: Session = Depends(get_db)):
    """Toggle resource active/inactive status"""
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.is_active = not resource.is_active
    db.commit()
    db.refresh(resource)
    
    return {
        "success": True,
        "message": f"Resource {'activated' if resource.is_active else 'deactivated'} successfully",
        "is_active": resource.is_active
    }

@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request, db: Session = Depends(get_db)):
    """หน้าจัดการ Resource DNA"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    return templates.TemplateResponse("resources.html", {
        "request": request,
        "resources": resources
    })

@app.get("/daily-tracking", response_class=HTMLResponse)
async def daily_tracking_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้า Daily Task Tracking"""
    projects = db.query(models.Project).all()
    
    # Filter tasks by project if specified
    if project_id:
        tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    else:
        tasks = db.query(models.Task).all()
    
    return templates.TemplateResponse("daily_tracking.html", {
        "request": request,
        "projects": projects,
        "tasks": tasks,
        "selected_project_id": project_id,
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/admin-tasks", response_class=HTMLResponse)
async def admin_tasks_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้า Admin & Procurement Tasks"""
    projects = db.query(models.Project).all()
    
    # Filter admin tasks
    query = db.query(models.Task).filter(
        models.Task.task_type.in_(['Admin', 'Procurement', 'PR', 'PO'])
    )
    
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    
    admin_tasks = query.all()
    
    return templates.TemplateResponse("admin_tasks.html", {
        "request": request,
        "projects": projects,
        "admin_tasks": admin_tasks,
        "selected_project_id": project_id
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, db: Session = Depends(get_db)):
    """หน้า Settings"""
    resource_count = db.query(models.Resource).filter(models.Resource.is_active == True).count()
    project_count = db.query(models.Project).count()
    
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "resource_count": resource_count,
        "project_count": project_count
    })

@app.get("/kanban", response_class=HTMLResponse)
async def kanban_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้า Kanban Board"""
    projects = db.query(models.Project).all()
    all_resources = db.query(models.Resource).all()  # Add resources for task display
    
    # Filter tasks by project if specified
    if project_id:
        tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    else:
        tasks = db.query(models.Task).all()
    
    return templates.TemplateResponse("kanban.html", {
        "request": request,
        "projects": projects,
        "tasks": tasks,
        "all_resources": all_resources,  # Add resources to template context
        "selected_project_id": project_id
    })

@app.get("/workload", response_class=HTMLResponse)
async def workload_page(request: Request, db: Session = Depends(get_db)):
    """หน้า Team Workload - แสดง Workload ของแต่ละ Resource (รองรับ Multi-Assign)"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    
    # คำนวณ workload สำหรับแต่ละ resource
    workload_data = []
    for resource in resources:
        # Get tasks from both old (assigned_resource_id) and new (task_resources) system
        tasks_old = db.query(models.Task).filter(models.Task.assigned_resource_id == resource.id).all()
        
        # Get tasks from multi-assign table
        task_ids_new = db.query(models.TaskResource.task_id).filter(
            models.TaskResource.resource_id == resource.id
        ).all()
        tasks_new = db.query(models.Task).filter(
            models.Task.id.in_([t.task_id for t in task_ids_new])
        ).all()
        
        # Combine and deduplicate
        all_tasks = {t.id: t for t in tasks_old + tasks_new}.values()
        tasks = list(all_tasks)
        
        workload_data.append({
            'resource': resource,
            'tasks': tasks,
            'task_count': len(tasks),
            'todo_count': len([t for t in tasks if t.actual_progress == 0]),
            'in_progress_count': len([t for t in tasks if 0 < t.actual_progress < 100]),
            'completed_count': len([t for t in tasks if t.actual_progress == 100])
        })
    
    # Sort by task count (descending)
    workload_data.sort(key=lambda x: x['task_count'], reverse=True)
    
    return templates.TemplateResponse("workload.html", {
        "request": request,
        "resources": resources,
        "workload_data": workload_data
    })

@app.get("/management-control", response_class=HTMLResponse)
async def management_control_page(request: Request, db: Session = Depends(get_db)):
    """Management Control Center - Hub for resource management"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    all_tasks = db.query(models.Task).all()
    
    # Calculate metrics
    total_resources = len(resources)
    active_resources = total_resources
    total_tasks = len(all_tasks)
    
    # Calculate workload distribution
    workload_counts = []
    resources_with_skills = 0
    total_speed = 0
    
    for resource in resources:
        # Count tasks
        tasks_old = db.query(models.Task).filter(models.Task.assigned_resource_id == resource.id).all()
        task_ids_new = db.query(models.TaskResource.task_id).filter(
            models.TaskResource.resource_id == resource.id
        ).all()
        tasks_new = db.query(models.Task).filter(
            models.Task.id.in_([t.task_id for t in task_ids_new])
        ).all()
        all_resource_tasks = {t.id: t for t in tasks_old + tasks_new}.values()
        task_count = len(list(all_resource_tasks))
        workload_counts.append(task_count)
        
        # Count skills
        if resource.skills:
            resources_with_skills += 1
        
        # Sum speed scores
        if resource.speed_score:
            total_speed += resource.speed_score
    
    # Calculate averages and counts
    avg_workload = sum(workload_counts) / total_resources if total_resources > 0 else 0
    avg_speed = total_speed / total_resources if total_resources > 0 else 0
    
    available_resources = len([w for w in workload_counts if w == 0])
    balanced_resources = len([w for w in workload_counts if 1 <= w <= 5])
    overloaded_count = len([w for w in workload_counts if w > 5])
    
    return templates.TemplateResponse("management_control.html", {
        "request": request,
        "total_resources": total_resources,
        "active_resources": active_resources,
        "total_tasks": total_tasks,
        "avg_workload": avg_workload,
        "overloaded_count": overloaded_count,
        "resources_with_skills": resources_with_skills,
        "avg_speed": avg_speed,
        "available_resources": available_resources,
        "balanced_resources": balanced_resources
    })


@app.get("/calendar", response_class=HTMLResponse)
async def calendar_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้า Calendar View - แสดง Tasks ตาม Timeline (List View)"""
    projects = db.query(models.Project).all()
    
    # Filter tasks by project if specified
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    
    tasks = query.all()
    
    # Categorize tasks by date
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_end = week_start + datetime.timedelta(days=6)
    next_week_start = week_end + datetime.timedelta(days=1)
    next_week_end = next_week_start + datetime.timedelta(days=6)
    
    upcoming_tasks = []
    this_week_tasks = []
    next_week_tasks = []
    overdue_tasks = []
    later_tasks = []
    
    for task in tasks:
        if task.planned_end:
            if task.planned_end < today and task.actual_progress < 100:
                overdue_tasks.append(task)
            elif week_start <= task.planned_end <= week_end:
                this_week_tasks.append(task)
            elif next_week_start <= task.planned_end <= next_week_end:
                next_week_tasks.append(task)
            elif task.planned_end > next_week_end:
                later_tasks.append(task)
            
            # Upcoming = next 30 days
            if task.planned_end >= today and task.planned_end <= today + datetime.timedelta(days=30):
                upcoming_tasks.append(task)
    
    # Sort by date
    upcoming_tasks.sort(key=lambda t: t.planned_end if t.planned_end else datetime.date.max)
    
    return templates.TemplateResponse("calendar.html", {
        "request": request,
        "projects": projects,
        "selected_project_id": project_id,
        "upcoming_tasks": upcoming_tasks[:10],  # Limit to 10
        "this_week_tasks": this_week_tasks,
        "next_week_tasks": next_week_tasks,
        "overdue_tasks": overdue_tasks,
        "later_tasks": later_tasks,
        "current_month": today.strftime("%B %Y")
    })

@app.get("/calendar-grid", response_class=HTMLResponse)
async def calendar_grid_page(
    request: Request,
    project_id: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """หน้า Calendar Grid - แสดง Tasks แบบปฏิทิน (Interactive Month Grid)"""
    import json
    
    projects = db.query(models.Project).all()
    
    # Default to current month/year
    today = datetime.date.today()
    current_month = month if month else today.month
    current_year = year if year else today.year
    
    # Filter tasks by project if specified
    query = db.query(models.Task).filter(
        models.Task.planned_start.isnot(None),
        models.Task.planned_end.isnot(None)
    )
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    
    tasks = query.all()
    
    # Convert to JSON for JavaScript
    tasks_json = json.dumps([{
        'id': t.id,
        'task_name': t.task_name,
        'task_type': t.task_type,
        'project_id': t.project_id,
        'planned_start': t.planned_start.strftime('%Y-%m-%d') if t.planned_start else None,
        'planned_end': t.planned_end.strftime('%Y-%m-%d') if t.planned_end else None,
        'actual_progress': float(t.actual_progress)
    } for t in tasks])
    
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    return templates.TemplateResponse("calendar_new.html", {
        "request": request,
        "projects": projects,
        "selected_project_id": project_id,
        "current_month": current_month,
        "current_year": current_year,
        "current_month_name": month_names[current_month - 1],
        "tasks_json": tasks_json
    })

@app.get("/gantt", response_class=HTMLResponse)
async def gantt_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้า Gantt Chart - แสดง Timeline ของ Tasks แบบ Gantt"""
    import json
    
    projects = db.query(models.Project).all()
    
    # Filter tasks by project if specified
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    
    # Only get tasks with planned dates
    tasks = query.filter(
        models.Task.planned_start.isnot(None),
        models.Task.planned_end.isnot(None)
    ).order_by(models.Task.planned_start).all()
    
    # Calculate date range
    date_range = {
        'start': None,
        'end': None,
        'duration': 0
    }
    
    if tasks:
        # Find min start and max end
        start_dates = [t.planned_start for t in tasks if t.planned_start]
        end_dates = [t.planned_end for t in tasks if t.planned_end]
        
        if start_dates and end_dates:
            min_date = min(start_dates)
            max_date = max(end_dates)
            
            # Add padding (1 week before/after)
            min_date = min_date - datetime.timedelta(days=7)
            max_date = max_date + datetime.timedelta(days=7)
            
            date_range['start'] = min_date.strftime('%Y-%m-%d')
            date_range['end'] = max_date.strftime('%Y-%m-%d')
            date_range['duration'] = (max_date - min_date).days
    
    # Convert tasks to JSON for JavaScript
    tasks_json = json.dumps([{
        'id': t.id,
        'task_name': t.task_name,
        'task_type': t.task_type,
        'project_id': t.project_id,
        'planned_start': t.planned_start.strftime('%Y-%m-%d') if t.planned_start else None,
        'planned_end': t.planned_end.strftime('%Y-%m-%d') if t.planned_end else None,
        'actual_progress': float(t.actual_progress),
        'assigned_resource_id': t.assigned_resource_id
    } for t in tasks])
    
    date_range_json = json.dumps(date_range)
    
    return templates.TemplateResponse("gantt.html", {
        "request": request,
        "projects": projects,
        "tasks": tasks,
        "selected_project_id": project_id,
        "date_range": date_range,
        "tasks_json": tasks_json,
        "date_range_json": date_range_json
    })

# ==================== Issue Management Routes ====================

@app.get("/issues", response_class=HTMLResponse)
async def issues_page(
    request: Request,
    project_id: Optional[int] = None,
    phase_id: Optional[int] = None,
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """หน้า Issue Management - แสดงรายการ Issues ทั้งหมด"""
    projects = db.query(models.Project).all()
    phases = db.query(models.ProjectPhase).all()
    
    # Build query
    query = db.query(models.Issue)
    
    if project_id:
        query = query.filter(models.Issue.project_id == project_id)
    if phase_id:
        query = query.filter(models.Issue.phase_id == phase_id)
    if status:
        query = query.filter(models.Issue.status == status)
    if severity:
        query = query.filter(models.Issue.severity == severity)
    
    issues = query.order_by(models.Issue.created_at.desc()).all()
    
    return templates.TemplateResponse("issues.html", {
        "request": request,
        "projects": projects,
        "phases": phases,
        "issues": issues,
        "selected_project_id": project_id
    })

@app.get("/issues/create", response_class=HTMLResponse)
async def create_issue_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้าสร้าง Issue ใหม่"""
    projects = db.query(models.Project).all()
    phases = db.query(models.ProjectPhase).all()
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    
    return templates.TemplateResponse("create_issue.html", {
        "request": request,
        "projects": projects,
        "phases": phases,
        "resources": resources,
        "selected_project_id": project_id
    })

@app.post("/issues/create")
async def create_issue_form(
    project_id: int = Form(...),
    phase_id: Optional[int] = Form(None),
    issue_title: str = Form(...),
    issue_description: Optional[str] = Form(None),
    issue_type: str = Form("Bug"),
    severity: str = Form("Medium"),
    priority: str = Form("Medium"),
    pic_resource_id: Optional[int] = Form(None),
    due_date: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """สร้าง Issue ใหม่"""
    issue = models.Issue(
        project_id=project_id,
        phase_id=phase_id if phase_id else None,
        issue_title=issue_title,
        issue_description=issue_description,
        issue_type=issue_type,
        severity=severity,
        priority=priority,
        status="Open",
        pic_resource_id=pic_resource_id if pic_resource_id else None,
        due_date=datetime.datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
    )
    db.add(issue)
    db.commit()
    db.refresh(issue)
    
    return RedirectResponse(url=f"/issues/{issue.id}", status_code=303)

@app.get("/issues/{issue_id}", response_class=HTMLResponse)
async def issue_details_page(issue_id: int, request: Request, db: Session = Depends(get_db)):
    """หน้ารายละเอียด Issue"""
    issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    comments = db.query(models.IssueComment).filter(
        models.IssueComment.issue_id == issue_id
    ).order_by(models.IssueComment.created_at.desc()).all()
    
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    phases = db.query(models.ProjectPhase).filter(
        models.ProjectPhase.project_id == issue.project_id
    ).all()
    
    return templates.TemplateResponse("issue_details.html", {
        "request": request,
        "issue": issue,
        "comments": comments,
        "resources": resources,
        "phases": phases
    })

@app.post("/issues/{issue_id}/update")
async def update_issue_form(
    issue_id: int,
    status: str = Form(...),
    severity: Optional[str] = Form(None),
    priority: Optional[str] = Form(None),
    pic_resource_id: Optional[int] = Form(None),
    resolution: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """อัพเดท Issue"""
    issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    old_status = issue.status
    issue.status = status
    if severity:
        issue.severity = severity
    if priority:
        issue.priority = priority
    if pic_resource_id:
        issue.pic_resource_id = pic_resource_id
    if resolution:
        issue.resolution = resolution
    
    # Update closed_at if closing
    if status == "Closed" and old_status != "Closed":
        issue.closed_at = datetime.datetime.utcnow()
    
    db.commit()
    
    return RedirectResponse(url=f"/issues/{issue_id}", status_code=303)

@app.post("/issues/{issue_id}/comment")
async def add_issue_comment(
    issue_id: int,
    comment_text: str = Form(...),
    comment_type: str = Form("comment"),
    user_name: str = Form("User"),
    db: Session = Depends(get_db)
):
    """เพิ่ม Comment/Note ให้ Issue"""
    comment = models.IssueComment(
        issue_id=issue_id,
        user_name=user_name,
        comment_text=comment_text,
        comment_type=comment_type
    )
    db.add(comment)
    db.commit()
    
    return RedirectResponse(url=f"/issues/{issue_id}", status_code=303)

@app.get("/phases", response_class=HTMLResponse)
async def phases_page(request: Request, project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """หน้าจัดการ Project Phases"""
    projects = db.query(models.Project).all()
    
    query = db.query(models.ProjectPhase)
    if project_id:
        query = query.filter(models.ProjectPhase.project_id == project_id)
    
    phases = query.order_by(models.ProjectPhase.project_id, models.ProjectPhase.phase_order).all()
    
    return templates.TemplateResponse("phases.html", {
        "request": request,
        "projects": projects,
        "phases": phases,
        "selected_project_id": project_id
    })

@app.post("/phases/create")
async def create_phase_form(
    project_id: int = Form(...),
    phase_name: str = Form(...),
    phase_order: int = Form(0),
    planned_start: Optional[str] = Form(None),
    planned_end: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """สร้าง Phase ใหม่"""
    phase = models.ProjectPhase(
        project_id=project_id,
        phase_name=phase_name,
        phase_order=phase_order,
        planned_start=datetime.datetime.strptime(planned_start, '%Y-%m-%d').date() if planned_start else None,
        planned_end=datetime.datetime.strptime(planned_end, '%Y-%m-%d').date() if planned_end else None,
        description=description,
        status="pending"
    )
    db.add(phase)
    db.commit()
    
    return RedirectResponse(url=f"/phases?project_id={project_id}", status_code=303)

# ==================== AI Assistant Routes ====================

@app.get("/ai-assistant", response_class=HTMLResponse)
async def ai_assistant_page(request: Request, db: Session = Depends(get_db)):
    """หน้า AI Assistant - AI-powered features"""
    projects = db.query(models.Project).all()
    
    return templates.TemplateResponse("ai_assistant.html", {
        "request": request,
        "projects": projects
    })

@app.post("/api/ai/breakdown-task")
async def ai_breakdown_task(
    task_name: str = Form(...),
    task_type: str = Form(...),
    start_date: str = Form(...),
    skip_weekends: bool = Form(True)
):
    """AI endpoint to break down a task into subtasks"""
    subtasks = ai_assistant.breakdown_task(task_name, task_type)
    
    # Add smart scheduling
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    scheduled = ai_assistant.suggest_schedule(subtasks, start, skip_weekends)
    
    return {
        "success": True,
        "subtasks": scheduled,
        "total_subtasks": len(scheduled),
        "total_days": sum(float(s["estimated_days"]) for s in scheduled)
    }

@app.get("/api/ai/recommend-resources")
async def ai_recommend_resources(
    task_type: str,
    skills: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """AI endpoint to recommend resources"""
    required_skills = skills.split(",") if skills else []
    recommendations = ai_assistant.recommend_resources(task_type, required_skills, db, top_n=5)
    
    return {
        "success": True,
        "recommendations": [
            {
                "resource_id": r["resource"].id,
                "resource_name": r["resource"].full_name,
                "position": r["resource"].position,
                "score": round(r["score"], 1),
                "match_percentage": round(r["match_percentage"], 1),
                "reasons": r["reasons"],
                "current_workload": r["current_workload"]
            }
            for r in recommendations
        ]
    }

@app.get("/api/ai/predict-risk/{task_id}")
async def ai_predict_risk(task_id: int, db: Session = Depends(get_db)):
    """AI endpoint to predict task risk"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    risk_assessment = ai_assistant.predict_risk(task, db)
    
    return {
        "success": True,
        "task_id": task_id,
        "task_name": task.task_name,
        **risk_assessment
    }

@app.get("/api/ai/project-insights/{project_id}")
async def ai_project_insights(project_id: int, db: Session = Depends(get_db)):
    """AI endpoint to generate project insights"""
    insights = ai_assistant.generate_insights(project_id, db)
    
    return {
        "success": True,
        "project_id": project_id,
        **insights
    }

# ==================== Backup/Restore Routes ====================

@app.get("/backup/download")
async def download_backup():
    """Download current database as backup"""
    import shutil
    from fastapi.responses import FileResponse
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"aiD_PM_backup_{timestamp}.db"
    
    # Create backup
    shutil.copy('pm_system.db', backup_file)
    
    return FileResponse(
        backup_file,
        filename=backup_file,
        media_type='application/x-sqlite3'
    )

@app.post("/backup/restore")
async def restore_backup(file: UploadFile = File(...)):
    """Restore database from backup file"""
    import shutil
    
    # Save uploaded file
    with open("pm_system_new.db", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Backup current DB
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy('pm_system.db', f'pm_system_backup_{timestamp}.db')
    
    # Replace with new DB
    shutil.move('pm_system_new.db', 'pm_system.db')
    
    return {"status": "success", "message": "Database restored successfully"}

@app.get("/projects/list", response_class=HTMLResponse)
async def projects_list_page(request: Request, db: Session = Depends(get_db)):
    """หน้ารายการโปรเจกต์ทั้งหมด"""
    projects = db.query(models.Project).all()
    current_week = datetime.date.today().isocalendar()[1]
    
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "projects": projects,
        "current_week": current_week
    })

@app.get("/projects/{project_id}/details", response_class=HTMLResponse)
async def project_details_page(project_id: int, request: Request, db: Session = Depends(get_db)):
    """หน้ารายละเอียดโปรเจกต์"""
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # ดึง Tasks ของโปรเจกต์
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    
    # คำนวณ Overall Progress (Value-Based)
    total_weight = sum(t.weight_score for t in tasks)
    weighted_progress = sum((t.actual_progress / 100) * t.weight_score for t in tasks)
    overall_progress = (weighted_progress / total_weight * 100) if total_weight > 0 else 0
    
    # ดึง Weekly Snapshots
    snapshots = db.query(models.WeeklySnapshot).filter(
        models.WeeklySnapshot.project_id == project_id
    ).order_by(models.WeeklySnapshot.week_number).all()
    
    # ดึง Project Phases
    phases = db.query(models.ProjectPhase).filter(
        models.ProjectPhase.project_id == project_id
    ).order_by(models.ProjectPhase.planned_start).all()
    
    # Calculate Timeline Boundaries
    timeline_start = None
    timeline_end = None
    if phases:
        starts = [p.planned_start for p in phases if p.planned_start]
        ends = [p.planned_end for p in phases if p.planned_end]
        if starts:
            timeline_start = min(starts)
        if ends:
            timeline_end = max(ends)
            
    # If no phases or dates, default to project creation date + 6 months
    if not timeline_start:
        timeline_start = project.created_at.date()
    if not timeline_end:
        timeline_end = timeline_start + datetime.timedelta(days=180)
        
    # Add buffer to timeline (1 week before, 1 week after)
    timeline_start = timeline_start - datetime.timedelta(days=7)
    timeline_end = timeline_end + datetime.timedelta(days=7)

    # Fetch Issues for this project
    issues = db.query(models.Issue).filter(models.Issue.project_id == project_id).all()
    
    return templates.TemplateResponse("project_details.html", {
        "request": request,
        "project": project,
        "tasks": tasks,
        "overall_progress": overall_progress,
        "snapshots": snapshots,
        "phases": phases,
        "timeline_start": timeline_start,
        "timeline_end": timeline_end,
        "issues": issues
    })

@app.get("/projects/{project_id}/history", response_class=HTMLResponse)
async def project_history(request: Request, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Get logs for this project OR tasks belonging to this project
    logs = db.query(models.ActivityLog).outerjoin(models.Task, models.ActivityLog.task_id == models.Task.id).filter(
        (models.ActivityLog.project_id == project_id) | 
        (models.Task.project_id == project_id)
    ).order_by(models.ActivityLog.created_at.desc()).all()
    
    return templates.TemplateResponse("project_history.html", {
        "request": request,
        "project": project,
        "logs": logs
    })

@app.get("/projects/create", response_class=HTMLResponse)
async def create_project_page(request: Request):
    """หน้าฟอร์มสร้างโปรเจกต์ใหม่"""
    return templates.TemplateResponse("create_project.html", {
        "request": request
    })

@app.get("/tasks/create", response_class=HTMLResponse)
async def create_task_page(request: Request, project_id: int, db: Session = Depends(get_db)):
    """หน้าฟอร์มสร้าง Task ใหม่"""
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    phases = db.query(models.ProjectPhase).filter(models.ProjectPhase.project_id == project_id).all()
    
    return templates.TemplateResponse("create_task.html", {
        "request": request,
        "project": project,
        "resources": resources,
        "phases": phases
    })

@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_page(task_id: int, request: Request, db: Session = Depends(get_db)):
    """หน้าฟอร์ม Edit Task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    phases = db.query(models.ProjectPhase).filter(models.ProjectPhase.project_id == task.project_id).all()
    
    # Get currently assigned resources (both primary and multi-assigned)
    assigned_resource_ids = set()
    
    # Primary assigned resource
    if task.assigned_resource_id:
        assigned_resource_ids.add(task.assigned_resource_id)
    
    # Multi-assigned resources
    task_resources = db.query(models.TaskResource).filter(
        models.TaskResource.task_id == task_id
    ).all()
    for tr in task_resources:
        assigned_resource_ids.add(tr.resource_id)
    
    return templates.TemplateResponse("edit_task.html", {
        "request": request,
        "task": task,
        "resources": resources,
        "phases": phases,
        "assigned_resource_ids": list(assigned_resource_ids)
    })

# ==================== Form Handlers ====================

@app.post("/resources/add")
async def add_resource(
    full_name: str = Form(...),
    nickname: str = Form(...),
    position: str = Form(...),
    speed: int = Form(...),
    quality: int = Form(...),
    company: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    # Skills will be received as a JSON string or we can parse form fields manually if dynamic
    # For simplicity, let's assume we receive a JSON string from a hidden input or similar
    skills_json: Optional[str] = Form(None), 
    db: Session = Depends(get_db)
):
    """เพิ่ม Resource ใหม่จากฟอร์ม"""
    new_res = models.Resource(
        full_name=full_name,
        nickname=nickname,
        position=position,
        speed_score=speed,
        quality_score=quality,
        company=company,
        comment=comment,
        skills=skills_json,
        is_active=True
    )
    db.add(new_res)
    db.commit()
    return RedirectResponse(url="/resources", status_code=303)

@app.post("/projects/create")
async def create_project_form(
    name: str = Form(...),
    customer: Optional[str] = Form(None),
    method: str = Form("Scrum"),
    budget_masked: Optional[str] = Form(None),
    is_recovery_mode: Optional[str] = Form(None),
    # Phase Data (received as list of strings/dates)
    phase_names: List[str] = Form([]),
    phase_starts: List[str] = Form([]),
    phase_ends: List[str] = Form([]),
    db: Session = Depends(get_db)
):
    """สร้างโปรเจกต์ใหม่พร้อม Phases และ Log"""
    # 1. Create Project
    project = models.Project(
        name=name,
        customer=customer,
        methodology=method,
        budget_masked=budget_masked,
        is_recovery_mode=(is_recovery_mode == "true")
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # 2. Create Phases
    # phase_names comes from the form. If using standard phases, we expect them in order.
    # The form might send empty strings for dates, need to handle that.
    
    for i, p_name in enumerate(phase_names):
        if not p_name.strip():
            continue
            
        p_start = None
        if i < len(phase_starts) and phase_starts[i]:
            try:
                p_start = datetime.datetime.strptime(phase_starts[i], '%Y-%m-%d').date()
            except:
                pass
                
        p_end = None
        if i < len(phase_ends) and phase_ends[i]:
            try:
                p_end = datetime.datetime.strptime(phase_ends[i], '%Y-%m-%d').date()
            except:
                pass
        
        phase = models.ProjectPhase(
            project_id=project.id,
            phase_name=p_name,
            phase_order=i+1,
            planned_start=p_start,
            planned_end=p_end,
            status="pending"
        )
        db.add(phase)
    
    # 3. Log Activity
    log = models.ActivityLog(
        project_id=project.id,
        action_type="project_created",
        description=f"Project '{name}' created with {len(phase_names)} phases.",
        user_name="System"
    )
    db.add(log)
    
    db.commit()
    return RedirectResponse(url=f"/projects/{project.id}/details", status_code=303)

@app.post("/tasks/create")
async def create_task_form(
    project_id: int = Form(...),
    task_name: str = Form(...),
    task_type: str = Form(...),
    weight_score: float = Form(...),
    resource_ids: List[int] = Form([]),  # Multi-select support
    phase_id: Optional[str] = Form(None),  # Accept as string first to validate
    planned_start: Optional[str] = Form(None),
    planned_end: Optional[str] = Form(None),
    next_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """สร้าง Task ใหม่จากฟอร์ม พร้อม Multi-Assign และ Phase"""
    # Handle phase_id validation (convert empty string to None)
    validated_phase_id = None
    if phase_id and phase_id.strip():
        try:
            validated_phase_id = int(phase_id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid phase ID")
    
    task = models.Task(
        project_id=project_id,
        task_name=task_name,
        task_type=task_type,
        weight_score=weight_score,
        assigned_resource_id=resource_ids[0] if resource_ids and len(resource_ids) > 0 else None,  # Safe access
        phase_id=validated_phase_id,  # Use validated phase ID
        planned_start=datetime.datetime.strptime(planned_start, '%Y-%m-%d').date() if planned_start else None,
        planned_end=datetime.datetime.strptime(planned_end, '%Y-%m-%d').date() if planned_end else None,
        actual_progress=0.0
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Add multi-assign relationships
    if resource_ids:  # Only if resources are selected
        for resource_id in resource_ids:
            task_resource = models.TaskResource(
                task_id=task.id,
                resource_id=resource_id
            )
            db.add(task_resource)
        db.commit()
    
    redirect_target = next_url if next_url else f"/projects/{project_id}/details"
    return RedirectResponse(url=redirect_target, status_code=303)

@app.post("/tasks/{task_id}/edit")
async def edit_task_form(
    task_id: int,
    task_name: str = Form(...),
    task_type: str = Form(...),
    weight_score: float = Form(...),
    actual_progress: float = Form(...),
    resource_ids: List[int] = Form([]),  # Multi-select support
    phase_id: Optional[str] = Form(None),  # Accept as string first to validate
    planned_start: Optional[str] = Form(None),
    planned_end: Optional[str] = Form(None),
    next_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """อัพเดท Task จากฟอร์ม พร้อม Multi-Assign และ Phase"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Handle phase_id validation (convert empty string to None)
    validated_phase_id = None
    if phase_id and phase_id.strip():
        try:
            validated_phase_id = int(phase_id)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid phase ID")
    
    task.task_name = task_name
    task.task_type = task_type
    task.weight_score = weight_score
    task.actual_progress = actual_progress
    task.assigned_resource_id = resource_ids[0] if resource_ids else None  # Primary
    task.phase_id = validated_phase_id  # Use validated phase ID
    task.planned_start = datetime.datetime.strptime(planned_start, '%Y-%m-%d').date() if planned_start else None
    task.planned_end = datetime.datetime.strptime(planned_end, '%Y-%m-%d').date() if planned_end else None
    
    # Update multi-assign: clear old, add new
    db.query(models.TaskResource).filter(models.TaskResource.task_id == task_id).delete()
    for resource_id in resource_ids:
        task_resource = models.TaskResource(
            task_id=task_id,
            resource_id=resource_id
        )
        db.add(task_resource)
    
    db.commit()
    redirect_target = next_url if next_url else f"/projects/{task.project_id}/details"
    return RedirectResponse(url=redirect_target, status_code=303)

@app.get("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """ลบ Task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    project_id = task.project_id
    db.delete(task)
    db.commit()
    return RedirectResponse(url=f"/projects/{project_id}/details", status_code=303)

# ==================== CSV Import/Export Endpoints ====================

import csv_handler
from fastapi.responses import Response

@app.get("/projects/{project_id}/tasks/export")
@app.get("/projects/{project_id}/export-csv")  # Backward compatibility alias
async def export_tasks_csv(project_id: int, db: Session = Depends(get_db)):
    """Export all tasks for a project as CSV file"""
    # Check if project exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get tasks count
    tasks_count = db.query(models.Task).filter(models.Task.project_id == project_id).count()
    
    # Generate CSV
    if tasks_count > 0:
        csv_content = csv_handler.export_tasks_to_csv(project_id, db)
    else:
        # Return blank template if no tasks
        csv_content = csv_handler.generate_blank_template()
    
    # Return as downloadable file
    filename = f"tasks_project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
    
    # Encode as UTF-8 with BOM for proper Unicode support
    csv_bytes = '\ufeff'.encode('utf-8') + csv_content.encode('utf-8')
    
    return Response(
        content=csv_bytes,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/projects/{project_id}/tasks/import")
async def import_tasks_csv(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import tasks from CSV file with strict validation"""
    # Check if project exists
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Read CSV content with better encoding handling
    try:
        csv_content = await file.read()
        # Try UTF-8 first, then fall back to other encodings
        try:
            csv_text = csv_content.decode('utf-8')
        except UnicodeDecodeError:
            # Try UTF-8 with BOM
            try:
                csv_text = csv_content.decode('utf-8-sig')
            except UnicodeDecodeError:
                # Fall back to Windows encoding
                try:
                    csv_text = csv_content.decode('cp1252')
                except UnicodeDecodeError:
                    # Last resort: ISO-8859-1
                    csv_text = csv_content.decode('iso-8859-1')
    except Exception as e:
        return {
            "status": "error",
            "success": False,
            "created_count": 0,
            "updated_count": 0,
            "errors": [f"File read error: {str(e)}"],
            "message": f"File read error: {str(e)}"
        }
    
    # Import tasks
    result = csv_handler.import_tasks_from_csv(project_id, csv_text, db)
    
    return result

# ==================== API Endpoints ====================

@app.get("/api/test")
def test_endpoint():
    """Simple test endpoint"""
    return {"status": "ok", "message": "Test endpoint working"}

@app.get("/api/find-resources")
def find_resources(q: str = "", db: Session = Depends(get_db)):
    """Find resources by full name, skills, and position only"""
    try:
        # Get all active resources
        resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
        
        results = []
        for r in resources:
            # Simple search - only check full_name, skills, and position
            if q:
                search_term = q.lower()
                full_name = r.full_name.lower() if r.full_name else ""
                skills = r.skills.lower() if r.skills else ""
                position = r.position.lower() if r.position else ""
                
                # Skip if no match
                if not (search_term in full_name or search_term in skills or search_term in position):
                    continue
            
            # Build result
            results.append({
                "id": r.id,
                "full_name": r.full_name,
                "nickname": r.nickname or "",
                "position": r.position or "",
                "company": r.company or "",
                "skills": r.skills or "",
                "is_active": r.is_active,
                "display_text": f"{r.full_name} ({r.nickname or 'No nickname'}) - {r.position or 'No position'}"
            })
        
        return results[:20]
        
    except Exception:
        return []

@app.get("/api/resources", response_model=List[ResourceResponse])
def api_get_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """API: ดึงรายการ Resources ทั้งหมด (สำหรับ dropdown)"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).offset(skip).limit(limit).all()
    return resources

@app.get("/api/recommend-resource/{task_type}")
async def api_recommend_resource(task_type: str, db: Session = Depends(get_db)):
    """API: แนะนำ Resource ตาม task_type (Hidden AI)"""
    return get_system_recommendation(task_type, db)

@app.post("/api/tasks/{task_id}/progress")
async def api_update_task_progress(task_id: int, progress: float = Form(...), db: Session = Depends(get_db)):
    """API: อัพเดทความคืบหน้าของ Task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_progress = task.actual_progress
    task.actual_progress = progress
    
    # Log activity
    activity = models.ActivityLog(
        task_id=task_id,
        action_type="status_changed",
        description=f"Progress updated from {old_progress}% to {progress}%",
        user_name="System"
    )
    db.add(activity)
    
    # --- Data Sync: Update Project Progress ---
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if project:
        # Recalculate project progress
        project_tasks = db.query(models.Task).filter(models.Task.project_id == project.id).all()
        if project_tasks:
            total_weight = sum(t.weight_score for t in project_tasks)
            # Note: We use the NEW progress for the current task, but it's already set in 'task' object
            # However, 'task' object in session might not be fully flushed for query re-fetch? 
            # Actually, since we modified 'task' which is attached to session, it should be fine.
            # Let's calculate manually to be safe and efficient without re-querying everything if possible,
            # but re-querying is safer for consistency.
            
            # Use the values from the list we just queried, which includes the updated task (because same session)
            weighted_progress = sum((t.actual_progress / 100) * t.weight_score for t in project_tasks)
            new_project_progress = (weighted_progress / total_weight * 100) if total_weight > 0 else 0
            
            project.progress = new_project_progress
            
    db.commit()
    return {"status": "success", "task_id": task_id, "progress": progress, "project_progress": project.progress if project else None}

@app.get("/api/tasks/{task_id}/comments")
async def get_task_comments(task_id: int, db: Session = Depends(get_db)):
    """API: ดึง Comments ของ Task"""
    comments = db.query(models.Comment).filter(models.Comment.task_id == task_id).order_by(models.Comment.created_at.desc()).all()
    return [
        {
            "id": c.id,
            "user_name": c.user_name,
            "comment_text": c.comment_text,
            "created_at": c.created_at.isoformat()
        }
        for c in comments
    ]

@app.post("/api/tasks/{task_id}/comments")
async def add_task_comment(task_id: int, comment_text: str = Form(...), user_name: str = Form("User"), db: Session = Depends(get_db)):
    """API: เพิ่ม Comment ให้ Task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    comment = models.Comment(
        task_id=task_id,
        user_name=user_name,
        comment_text=comment_text
    )
    db.add(comment)
    
    # Log activity
    activity = models.ActivityLog(
        task_id=task_id,
        action_type="commented",
        description=f"{user_name} added a comment",
        user_name=user_name
    )
    db.add(activity)
    
    db.commit()
    db.refresh(comment)
    
    return {
        "status": "success",
        "comment_id": comment.id,
        "created_at": comment.created_at.isoformat()
    }

@app.get("/api/tasks")
async def get_tasks_by_project(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """API: ดึง Tasks ตาม Project"""
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    
    tasks = query.all()
    return {
        "tasks": [
            {
                "id": t.id,
                "task_name": t.task_name,
                "task_type": t.task_type,
                "actual_progress": float(t.actual_progress),
                "planned_start": t.planned_start.strftime("%Y-%m-%d") if t.planned_start else None,
                "planned_end": t.planned_end.strftime("%Y-%m-%d") if t.planned_end else None
            }
            for t in tasks
        ]
    }

@app.get("/api/tasks/{task_id}/activity")
async def get_task_activity(task_id: int, db: Session = Depends(get_db)):
    """API: ดึง Activity Log ของ Task"""
    activities = db.query(models.ActivityLog).filter(models.ActivityLog.task_id == task_id).order_by(models.ActivityLog.created_at.desc()).limit(50).all()
    return [
        {
            "id": a.id,
            "action_type": a.action_type,
            "description": a.description,
            "user_name": a.user_name,
            "created_at": a.created_at.isoformat()
        }
        for a in activities
    ]

@app.post("/projects/{project_id}/take-snapshot")
async def take_weekly_snapshot(project_id: int, db: Session = Depends(get_db)):
    """
    สร้าง Weekly Snapshot จากความคืบหน้าปัจจุบัน
    คำนวณแบบ Value-Based (Weighted Progress)
    """
    # 1. ดึงงานทั้งหมดในโปรเจกต์
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this project")
    
    # 2. คำนวณ % สะสมแบบถ่วงน้ำหนัก (Weighted Progress)
    total_weight = sum(t.weight_score for t in tasks)
    actual_weighted = sum((t.actual_progress / 100) * t.weight_score for t in tasks)
    
    actual_acc_percent = (actual_weighted / total_weight) * 100 if total_weight > 0 else 0
    
    # 3. หา Week Number ปัจจุบัน (ISO week)
    current_week = datetime.date.today().isocalendar()[1]
    
    # 4. ตรวจสอบว่ามี snapshot สัปดาห์นี้แล้วหรือยัง
    existing_snapshot = db.query(models.WeeklySnapshot).filter(
        models.WeeklySnapshot.project_id == project_id,
        models.WeeklySnapshot.week_number == current_week
    ).first()
    
    if existing_snapshot:
        # อัพเดทของเดิม
        existing_snapshot.actual_acc = actual_acc_percent
        db.commit()
        return {"status": "updated", "actual_acc": actual_acc_percent, "week_number": current_week}
    else:
        # สร้างใหม่
        new_snapshot = models.WeeklySnapshot(
            project_id=project_id,
            week_number=current_week,
            actual_acc=actual_acc_percent,
            plan_acc=85.5  # ค่าแผนงานนี้อาจดึงมาจาก Master Plan ใน DB
        )
        db.add(new_snapshot)
        db.commit()
        return {"status": "created", "actual_acc": actual_acc_percent, "week_number": current_week}

# ==================== Original API Endpoints (จากเดิม) ====================

@app.post("/resources", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """API: สร้าง Resource ใหม่"""
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.get("/resources-list", response_model=List[ResourceResponse])
def get_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """API: ดึงรายการ Resources ทั้งหมด"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).offset(skip).limit(limit).all()
    return resources

@app.get("/resources/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """API: ดึงข้อมูล Resource ตาม ID"""
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.put("/resources/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, resource_update: ResourceCreate, db: Session = Depends(get_db)):
    """API: อัพเดทข้อมูล Resource"""
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    for key, value in resource_update.dict().items():
        setattr(db_resource, key, value)
    
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """API: ลบ Resource (Soft Delete)"""
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db_resource.is_active = False
    db.commit()
    return {"message": "Resource deactivated successfully"}

@app.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """API: สร้างโปรเจกต์ใหม่"""
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """API: ดึงรายการโปรเจกต์ทั้งหมด"""
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """API: ดึงข้อมูลโปรเจกต์ตาม ID"""
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectCreate, db: Session = Depends(get_db)):
    """API: อัพเดทข้อมูลโปรเจกต์"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project_update.dict().items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """API: สร้าง Task ใหม่"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """API: ดึงรายการ Tasks (ตัวกรองตามโปรเจกต์ได้)"""
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    tasks = query.all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """API: ดึงข้อมูล Task ตาม ID"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """API: อัพเดท Task Progress หรือ Assigned Resource"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/{task_id}/suggest-resource")
def get_suggested_resource(task_id: int, db: Session = Depends(get_db)):
    """API: แนะนำ Resource ที่เหมาะสมสำหรับ Task (AI Matching)"""
    suggestion = suggest_best_resource(db, task_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="No suitable resource found")
    return suggestion

@app.post("/weekly-snapshots", response_model=WeeklySnapshotResponse)
def create_weekly_snapshot(snapshot: WeeklySnapshotCreate, db: Session = Depends(get_db)):
    """API: สร้าง Weekly Snapshot สำหรับ PB Curve"""
    db_snapshot = models.WeeklySnapshot(**snapshot.dict())
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot

@app.get("/weekly-snapshots", response_model=List[WeeklySnapshotResponse])
def get_weekly_snapshots(project_id: int, db: Session = Depends(get_db)):
    """API: ดึงรายการ Weekly Snapshots ของโปรเจกต์"""
    snapshots = db.query(models.WeeklySnapshot).filter(
        models.WeeklySnapshot.project_id == project_id
    ).order_by(models.WeeklySnapshot.week_number).all()
    return snapshots

@app.post("/phases/{phase_id}/toggle-recovery")
async def toggle_phase_recovery(phase_id: int, db: Session = Depends(get_db)):
    phase = db.query(models.ProjectPhase).filter(models.ProjectPhase.id == phase_id).first()
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
        
    phase.is_recovery_mode = not phase.is_recovery_mode
    
    # Log Activity
    action = "entered" if phase.is_recovery_mode else "exited"
    log = models.ActivityLog(
        project_id=phase.project_id,
        action_type="phase_update",
        description=f"Phase '{phase.phase_name}' {action} Recovery Mode (Crisis Control).",
        user_name="System"
    )
    db.add(log)
    db.commit()
    
    return {"status": "success", "is_recovery_mode": phase.is_recovery_mode}

# ==================== Excel Export ====================

@app.get("/export/weekly/{project_id}")
def export_weekly_report_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Weekly Report เป็น Excel"""
    template_path = "templates_excel/WeeklyReport_PH(PU).xlsx"
    output_path = f"exports/WeeklyReport_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    try:
        result_path = excel_engine.export_weekly_report(db, project_id, template_path, output_path)
        return FileResponse(result_path, filename=os.path.basename(result_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/export/daily/{project_id}")
def export_daily_progress_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Daily Progress Report เป็น Excel"""
    template_path = "templates_excel/Daily_Progress_PH(PU).xls"
    output_path = f"exports/DailyProgress_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    try:
        result_path = excel_engine.export_daily_progress(db, project_id, template_path, output_path)
        return FileResponse(result_path, filename=os.path.basename(result_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

# ==================== Server Run ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
