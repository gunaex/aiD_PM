from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import datetime
import os

import models
from database import engine, get_db, init_db
import excel_engine

# สร้างตารางในฐานข้อมูล
init_db()

app = FastAPI(title="Smart PM Control Tower", version="1.0.0")

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

# ==================== API Endpoints ====================

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Smart PM Control Tower",
        "version": "1.0.0",
        "endpoints": {
            "resources": "/resources",
            "projects": "/projects",
            "tasks": "/tasks",
            "weekly_snapshots": "/weekly-snapshots"
        }
    }

# ==================== Resources CRUD ====================

@app.post("/resources", response_model=ResourceResponse)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """สร้าง Resource ใหม่"""
    db_resource = models.Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@app.get("/resources", response_model=List[ResourceResponse])
def get_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ดึงรายการ Resources ทั้งหมด"""
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).offset(skip).limit(limit).all()
    return resources

@app.get("/resources/{resource_id}", response_model=ResourceResponse)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูล Resource ตาม ID"""
    resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@app.put("/resources/{resource_id}", response_model=ResourceResponse)
def update_resource(resource_id: int, resource_update: ResourceCreate, db: Session = Depends(get_db)):
    """อัพเดทข้อมูล Resource"""
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
    """ลบ Resource (Soft Delete)"""
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db_resource.is_active = False
    db.commit()
    return {"message": "Resource deactivated successfully"}

# ==================== Projects CRUD ====================

@app.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """สร้างโปรเจกต์ใหม่"""
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects", response_model=List[ProjectResponse])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ดึงรายการโปรเจกต์ทั้งหมด"""
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูลโปรเจกต์ตาม ID"""
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectCreate, db: Session = Depends(get_db)):
    """อัพเดทข้อมูลโปรเจกต์"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in project_update.dict().items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

# ==================== Tasks CRUD ====================

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """สร้าง Task ใหม่"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(project_id: Optional[int] = None, db: Session = Depends(get_db)):
    """ดึงรายการ Tasks (ตัวกรองตามโปรเจกต์ได้)"""
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    tasks = query.all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูล Task ตาม ID"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """อัพเดท Task Progress หรือ Assigned Resource"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# ==================== Smart Matching ====================

@app.get("/tasks/{task_id}/suggest-resource")
def get_suggested_resource(task_id: int, db: Session = Depends(get_db)):
    """แนะนำ Resource ที่เหมาะสมสำหรับ Task (AI Matching)"""
    suggestion = suggest_best_resource(db, task_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="No suitable resource found")
    return suggestion

# ==================== Weekly Snapshots ====================

@app.post("/weekly-snapshots", response_model=WeeklySnapshotResponse)
def create_weekly_snapshot(snapshot: WeeklySnapshotCreate, db: Session = Depends(get_db)):
    """สร้าง Weekly Snapshot สำหรับ PB Curve"""
    db_snapshot = models.WeeklySnapshot(**snapshot.dict())
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot

@app.get("/weekly-snapshots", response_model=List[WeeklySnapshotResponse])
def get_weekly_snapshots(project_id: int, db: Session = Depends(get_db)):
    """ดึงรายการ Weekly Snapshots ของโปรเจกต์"""
    snapshots = db.query(models.WeeklySnapshot).filter(
        models.WeeklySnapshot.project_id == project_id
    ).order_by(models.WeeklySnapshot.week_number).all()
    return snapshots

# ==================== Excel Export ====================

@app.get("/export/weekly-report/{project_id}")
def export_weekly_report_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Weekly Report เป็น Excel"""
    template_path = "templates_excel/WeeklyReport_PH(PU).xlsx"
    output_path = f"output/WeeklyReport_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    os.makedirs("output", exist_ok=True)
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    try:
        result_path = excel_engine.export_weekly_report(db, project_id, template_path, output_path)
        return FileResponse(result_path, filename=os.path.basename(result_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/export/daily-progress/{project_id}")
def export_daily_progress_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Daily Progress Report เป็น Excel"""
    template_path = "templates_excel/Daily_Progress_PH(PU).xls"
    output_path = f"output/DailyProgress_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    
    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    os.makedirs("output", exist_ok=True)
    
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

