# Context for Copilot - Smart PM Control Tower

## 🎯 Project Overview

**Project Name:** Smart PM Control Tower (AID_PM)  
**Purpose:** AI-powered Project Management System with intelligent resource matching and automated Excel reporting

---

## 🏗️ Core Architecture

### Data Flow
```
User → Web UI (FastAPI) → SQLite Database (pm_system.db) → Excel Reports
                ↓
         AI Smart Matching
```

### Key Components

1. **Data Source:** SQLite database (`pm_system.db`)
2. **Backend:** FastAPI with SQLAlchemy ORM
3. **Intelligence:** Hidden AI for resource-task matching
4. **Output:** Excel reports from existing templates

---

## 📊 Database Schema

### Resources (บุคลากร)
- `id`: Primary Key
- `full_name`: ชื่อเต็ม (Required)
- `nickname`: ชื่อเล่น
- `position`: ตำแหน่ง
- `skills`: JSON - {"Python": 9, "SQL": 7}
- `speed_score`: 1-10 (ความเร็ว)
- `quality_score`: 1-10 (คุณภาพ)
- `is_active`: Boolean (Soft Delete)

### Projects (โปรเจกต์)
- `id`: Primary Key
- `name`: ชื่อโปรเจกต์ (Required)
- `customer`: ลูกค้า
- `methodology`: Waterfall, Scrum, Kanban
- `is_recovery_mode`: Boolean (โหมดกู้วิกฤต)
- `budget_masked`: String (฿฿฿)
- `created_at`: DateTime

### Tasks (งาน)
- `id`: Primary Key
- `project_id`: Foreign Key → Projects
- `task_name`: ชื่องาน
- `task_type`: Dev, Admin, Procurement (PR/PO)
- `weight_score`: Float (ค่าน้ำหนักสำหรับคำนวณ % Progress)
- `planned_start`: Date
- `planned_end`: Date
- `actual_progress`: Float 0-100
- `assigned_resource_id`: Foreign Key → Resources (Nullable)
- `ai_risk_score`: Float (Hidden Intelligence)

### WeeklySnapshot (สำหรับ PB Curve)
- `id`: Primary Key
- `project_id`: Foreign Key → Projects
- `week_number`: Integer
- `plan_acc`: Float (Accumulated Plan %)
- `actual_acc`: Float (Accumulated Actual %)

---

## 🤖 AI Smart Matching Logic

### Function: `calculate_matching_score(resource, task)`

**Input:**
- Resource object (with skills, speed_score, quality_score)
- Task object (with task_type)

**Logic:**
1. **Skill Match** (0-50 points):
   - ถ้า task_type ตรงกับ skill name → skill_level × 5
   - Example: Task type "Dev", Resource has {"Python": 9} → 9 × 5 = 45 points

2. **Speed Score** (0-25 points):
   - speed_score × 2.5
   - Example: speed_score = 8 → 8 × 2.5 = 20 points

3. **Quality Score** (0-25 points):
   - quality_score × 2.5
   - Example: quality_score = 9 → 9 × 2.5 = 22.5 points

**Output:** Score 0-100 (ซ่อนจากผู้ใช้)

### Function: `suggest_best_resource(db, task_id)`

**Process:**
1. Query task by ID
2. Get all active resources
3. Calculate matching score for each resource
4. Sort by score (descending)
5. Return top resource with score

**Output:**
```json
{
  "resource_id": 3,
  "full_name": "วิทยา เทคโนโลยี",
  "nickname": "วิท",
  "score": 82.5
}
```

---

## 📄 Excel Export Engine

### Templates Location
- `templates_excel/Daily_Progress_PH(PU).xls`
- `templates_excel/WeeklyReport_PH(PU).xlsx`

### Export Functions

#### 1. `export_weekly_report(db, project_id, template_path, output_path)`

**Purpose:** สร้าง Weekly Report พร้อม PB Curve

**Process:**
1. Load template workbook
2. Query WeeklySnapshots for project
3. Find "PB Curve" sheet
4. Write data starting at row 41:
   - Column B: week_number
   - Column C: plan_acc
   - Column D: actual_acc
5. Save to output path

#### 2. `export_daily_progress(db, project_id, template_path, output_path)`

**Purpose:** สร้าง Daily Progress Report

**Process:**
1. Load template workbook
2. Query Tasks for project
3. Fill data into template
4. Save to output path

---

## 🎨 Design Philosophy

### UI/UX Guidelines
- **Style:** Professional BI Dashboard (Dark/Slate theme)
- **Framework:** Tailwind CSS
- **No AI Icons:** ซ่อน AI ไว้เบื้องหลัง
- **Selectable Lists:** ไม่ให้พิมพ์ชื่อ Resource (เลือกจาก dropdown)

### Value-Based Tracking
- ใช้ `weight_score` ในการคำนวณ % Progress
- Formula: `Σ(task.actual_progress × task.weight_score) / Σ(task.weight_score)`

### Hidden Intelligence
- AI ทำงานเบื้องหลัง ไม่แสดงคะแนนให้ผู้ใช้เห็น
- แสดงเฉพาะ "แนะนำ" Resource ที่เหมาะสม

---

## 🔌 API Endpoints Summary

### Resources
- `POST /resources` - สร้าง
- `GET /resources` - ดึงทั้งหมด
- `GET /resources/{id}` - ดึงตาม ID
- `PUT /resources/{id}` - อัพเดท
- `DELETE /resources/{id}` - ลบ (Soft)

### Projects
- `POST /projects` - สร้าง
- `GET /projects` - ดึงทั้งหมด
- `GET /projects/{id}` - ดึงตาม ID
- `PUT /projects/{id}` - อัพเดท

### Tasks
- `POST /tasks` - สร้าง
- `GET /tasks?project_id={id}` - ดึงตามโปรเจกต์
- `GET /tasks/{id}` - ดึงตาม ID
- `PUT /tasks/{id}` - อัพเดท Progress/Resource
- `GET /tasks/{id}/suggest-resource` - 🤖 AI แนะนำ

### Weekly Snapshots
- `POST /weekly-snapshots` - บันทึก
- `GET /weekly-snapshots?project_id={id}` - ดึงตามโปรเจกต์

### Excel Export
- `GET /export/weekly-report/{project_id}` - ส่งออก Weekly
- `GET /export/daily-progress/{project_id}` - ส่งออก Daily

---

## 🚀 Development Workflow

### 1. Create New Feature
```python
# Add to main.py
@app.post("/new-endpoint")
def new_feature(db: Session = Depends(get_db)):
    # Implementation
    pass
```

### 2. Add Database Model
```python
# Add to models.py
class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    # ... fields
```

### 3. Update Excel Engine
```python
# Add to excel_engine.py
def export_new_report(db, project_id, template_path, output_path):
    # Implementation
    pass
```

---

## 🎯 Next Steps (Future Development)

- [ ] Web UI (Frontend) with Tailwind CSS
- [ ] Real-time Dashboard with WebSocket
- [ ] Advanced Analytics & Charts
- [ ] Multi-user Authentication
- [ ] Email Notifications
- [ ] Mobile App

---

## 📝 Important Notes

### For Copilot Chat
- Always use **Selectable Lists** for Resource assignment
- Never show AI scores to users
- Calculate progress using **weight_score**
- Daily updates → aggregate to **WeeklySnapshot**
- Excel templates are **read-only** (don't modify originals)

### For Code Generation
- Follow FastAPI best practices
- Use Pydantic for validation
- Implement proper error handling
- Add docstrings to all functions
- Use type hints

---

**Last Updated:** 2024-12-24  
**Version:** 1.0.0  
**Status:** Foundation Complete ✅

