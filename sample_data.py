"""
Script สำหรับสร้างข้อมูลตัวอย่าง (Sample Data)
รันไฟล์นี้เพื่อเติมข้อมูลทดสอบลงในระบบ
"""
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models
import datetime

def create_sample_data():
    """สร้างข้อมูลตัวอย่างสำหรับทดสอบระบบ"""
    db = SessionLocal()
    
    try:
        print("Creating sample data...")
        
        # 1. สร้าง Resources (บุคลากร)
        print("\n[1/4] Creating Resources...")
        resources = [
            models.Resource(
                full_name="สมชาย ใจดี",
                nickname="ชาย",
                position="Senior Developer",
                skills={"Python": 9, "SQL": 8, "FastAPI": 8, "React": 6},
                speed_score=8,
                quality_score=9,
                is_active=True
            ),
            models.Resource(
                full_name="สมหญิง รักงาน",
                nickname="หญิง",
                position="Project Manager",
                skills={"Project Management": 9, "Communication": 9, "Excel": 8},
                speed_score=7,
                quality_score=9,
                is_active=True
            ),
            models.Resource(
                full_name="วิทยา เทคโนโลยี",
                nickname="วิท",
                position="Full Stack Developer",
                skills={"Python": 7, "JavaScript": 8, "SQL": 7, "Docker": 6},
                speed_score=9,
                quality_score=7,
                is_active=True
            ),
            models.Resource(
                full_name="อนันต์ การเงิน",
                nickname="นันท์",
                position="Business Analyst",
                skills={"Analysis": 8, "Excel": 9, "Procurement": 7},
                speed_score=6,
                quality_score=8,
                is_active=True
            ),
        ]
        
        for resource in resources:
            db.add(resource)
        db.commit()
        print(f"   Created {len(resources)} resources")
        
        # 2. สร้าง Project
        print("\n[2/4] Creating Project...")
        project = models.Project(
            name="Smart PM Control Tower",
            customer="Internal - Digital Transformation Team",
            methodology="Scrum",
            is_recovery_mode=False,
            budget_masked="฿฿฿฿",
            created_at=datetime.datetime.utcnow()
        )
        db.add(project)
        db.commit()
        print(f"   Created project: {project.name} (ID: {project.id})")
        
        # 3. สร้าง Tasks
        print("\n[3/4] Creating Tasks...")
        tasks = [
            models.Task(
                project_id=project.id,
                task_name="Design Database Schema",
                task_type="Dev",
                weight_score=3.0,
                planned_start=datetime.date(2024, 1, 1),
                planned_end=datetime.date(2024, 1, 5),
                actual_progress=100.0,
                assigned_resource_id=1  # สมชาย
            ),
            models.Task(
                project_id=project.id,
                task_name="Develop FastAPI Backend",
                task_type="Dev",
                weight_score=8.0,
                planned_start=datetime.date(2024, 1, 6),
                planned_end=datetime.date(2024, 1, 20),
                actual_progress=75.0,
                assigned_resource_id=1  # สมชาย
            ),
            models.Task(
                project_id=project.id,
                task_name="Create Excel Export Engine",
                task_type="Dev",
                weight_score=5.0,
                planned_start=datetime.date(2024, 1, 15),
                planned_end=datetime.date(2024, 1, 25),
                actual_progress=60.0,
                assigned_resource_id=3  # วิทยา
            ),
            models.Task(
                project_id=project.id,
                task_name="Develop Web UI Dashboard",
                task_type="Dev",
                weight_score=10.0,
                planned_start=datetime.date(2024, 1, 20),
                planned_end=datetime.date(2024, 2, 10),
                actual_progress=20.0,
                assigned_resource_id=3  # วิทยา
            ),
            models.Task(
                project_id=project.id,
                task_name="Procurement - Server Hardware",
                task_type="Procurement",
                weight_score=2.0,
                planned_start=datetime.date(2024, 1, 10),
                planned_end=datetime.date(2024, 1, 30),
                actual_progress=50.0,
                assigned_resource_id=4  # อนันต์
            ),
            models.Task(
                project_id=project.id,
                task_name="Project Documentation",
                task_type="Admin",
                weight_score=3.0,
                planned_start=datetime.date(2024, 1, 1),
                planned_end=datetime.date(2024, 2, 15),
                actual_progress=40.0,
                assigned_resource_id=2  # สมหญิง
            ),
        ]
        
        for task in tasks:
            db.add(task)
        db.commit()
        print(f"   Created {len(tasks)} tasks")
        
        # 4. สร้าง Weekly Snapshots (สำหรับ PB Curve)
        print("\n[4/4] Creating Weekly Snapshots...")
        snapshots = [
            models.WeeklySnapshot(project_id=project.id, week_number=1, plan_acc=10.0, actual_acc=8.0),
            models.WeeklySnapshot(project_id=project.id, week_number=2, plan_acc=20.0, actual_acc=18.0),
            models.WeeklySnapshot(project_id=project.id, week_number=3, plan_acc=35.0, actual_acc=30.0),
            models.WeeklySnapshot(project_id=project.id, week_number=4, plan_acc=50.0, actual_acc=45.0),
            models.WeeklySnapshot(project_id=project.id, week_number=5, plan_acc=65.0, actual_acc=55.0),
        ]
        
        for snapshot in snapshots:
            db.add(snapshot)
        db.commit()
        print(f"   Created {len(snapshots)} weekly snapshots")
        
        print("\n" + "="*60)
        print("Sample data created successfully!")
        print("="*60)
        print("\nYou can now:")
        print("1. Run the server: python main.py")
        print("2. Access API docs: http://localhost:8000/docs")
        print("3. Test AI matching: GET /tasks/1/suggest-resource")
        print("4. Export reports: GET /export/weekly-report/1")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # ตรวจสอบว่าฐานข้อมูลมีอยู่แล้วหรือไม่
    init_db()
    create_sample_data()

