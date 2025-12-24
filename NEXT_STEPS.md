# 🚀 Next Steps - aiD_PM Development Roadmap

## ปัจจุบัน: ✅ Foundation + UI Complete (v1.1.0)

คุณมีระบบที่พร้อมใช้งานแล้ว:
- ✅ Database Layer (4 tables)
- ✅ API Layer (20+ endpoints)
- ✅ UI Layer (3 pages - Dashboard, Resources, Daily Tracking)
- ✅ AI Smart Matching
- ✅ Weekly Snapshots
- ✅ Excel Export

---

## 🎯 Phase 2: Complete CRUD Pages (แนะนำทำต่อ)

### 1. **Task Registration Page** 📝
**Priority:** ⭐⭐⭐⭐⭐ (สูงสุด)

**Why:** ตอนนี้ยังไม่มีหน้าสำหรับสร้างงานใหม่ผ่าน UI

**Copilot Prompt:**
```
Create a Task Registration page for aiD_PM:
1. Form fields: Task Name (text), Task Type (dropdown: Dev/Admin/Procurement), 
   Weight Score (number), Planned Start (date), Planned End (date)
2. Assignee: Searchable dropdown fetching from /api/resources
3. Dynamic: When Task Type selected, fetch from /api/recommend-resource/{task_type} 
   and show suggestion in subtle info box
4. Submit: POST to /tasks endpoint
5. Theme: Match existing Slate Dark dashboard
6. Include form validation
```

**Expected File:** `templates/task_create.html`

---

### 2. **Project Details Page** 📊
**Priority:** ⭐⭐⭐⭐ (สูง)

**Why:** ต้องการดูรายละเอียดโปรเจกต์แต่ละตัว พร้อม Tasks ทั้งหมด

**Features:**
- แสดง Project Info (Name, Customer, Methodology)
- ตาราง Tasks ในโปรเจกต์นั้นๆ
- Overall Progress Bar (คำนวณจาก Weight Score)
- Quick Actions: Add Task, Export Weekly, Export Daily
- PB Curve Mini Chart (ถ้ามีข้อมูล snapshots)

**Endpoint ที่ต้องเพิ่ม:**
```python
@app.get("/projects/{project_id}/details", response_class=HTMLResponse)
async def project_details(project_id: int, request: Request, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    tasks = db.query(models.Task).filter(models.Task.project_id == project_id).all()
    snapshots = db.query(models.WeeklySnapshot).filter(
        models.WeeklySnapshot.project_id == project_id
    ).order_by(models.WeeklySnapshot.week_number).all()
    
    # Calculate overall progress
    total_weight = sum(t.weight_score for t in tasks)
    weighted_progress = sum((t.actual_progress / 100) * t.weight_score for t in tasks)
    overall_progress = (weighted_progress / total_weight * 100) if total_weight > 0 else 0
    
    return templates.TemplateResponse("project_details.html", {
        "request": request,
        "project": project,
        "tasks": tasks,
        "snapshots": snapshots,
        "overall_progress": overall_progress
    })
```

---

### 3. **Admin Tasks Page** 🚨
**Priority:** ⭐⭐⭐ (กลาง)

**Why:** เน้นแสดงงาน PR/PO/Procurement ที่เป็น Blocker

**Features:**
- แสดงเฉพาะ task_type = Admin/Procurement/PR/PO
- ไฮไลต์งานที่ progress < 50% (สีแดง)
- แสดง Days Since Created
- Quick Update Progress
- Filter by Project

---

### 4. **Create Project Page** 🆕
**Priority:** ⭐⭐⭐ (กลาง)

**Why:** ตอนนี้มีแค่ form handler แต่ยังไม่มีหน้า UI

**Form Fields:**
- Project Name *
- Customer
- Methodology (Dropdown: Waterfall, Scrum, Kanban)
- Recovery Mode (Checkbox)
- Budget Masked (Text: ฿฿฿)

**Endpoint:** มีแล้วที่ `POST /projects/create` แค่สร้างหน้า HTML

---

## 🎨 Phase 3: Enhanced UI/UX

### 1. **Visual PB Curve Chart** 📈
**Library:** Chart.js หรือ ApexCharts

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<canvas id="pbCurve"></canvas>
<script>
const ctx = document.getElementById('pbCurve').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [1, 2, 3, 4, 5], // week numbers
        datasets: [{
            label: 'Plan',
            data: [10, 20, 35, 50, 65],
            borderColor: 'rgb(59, 130, 246)'
        }, {
            label: 'Actual',
            data: [8, 18, 30, 45, 55],
            borderColor: 'rgb(34, 197, 94)'
        }]
    }
});
</script>
```

---

### 2. **Resource Utilization Dashboard** 👥
แสดงภาระงานของแต่ละคน:
- กี่งานที่รับผิดชอบ
- รวม Weight Score
- Average Progress
- Workload Indicator (Low/Medium/High)

---

### 3. **Calendar View** 📅
แสดงงานในรูปแบบปฏิทิน:
- ใช้ FullCalendar.js
- แสดง planned_start และ planned_end
- สีตาม task_type
- คลิกดูรายละเอียดได้

---

### 4. **Gantt Chart** 📊
Timeline visualization:
- ใช้ DHTMLX Gantt หรือ Frappe Gantt
- แสดง Task dependencies (ถ้ามี)
- Drag & Drop update dates

---

## 🧠 Phase 4: Advanced AI Features

### 1. **Risk Prediction** ⚠️
คำนวณความเสี่ยงของ Task:
```python
def calculate_risk_score(task: models.Task, db: Session) -> float:
    risk = 0.0
    
    # Factor 1: Days overdue
    if task.planned_end and datetime.date.today() > task.planned_end:
        days_overdue = (datetime.date.today() - task.planned_end).days
        risk += days_overdue * 5
    
    # Factor 2: Progress vs Time
    if task.planned_start and task.planned_end:
        total_days = (task.planned_end - task.planned_start).days
        elapsed_days = (datetime.date.today() - task.planned_start).days
        expected_progress = (elapsed_days / total_days) * 100
        progress_gap = expected_progress - task.actual_progress
        if progress_gap > 0:
            risk += progress_gap * 2
    
    # Factor 3: Resource mismatch
    if task.assigned_resource_id:
        resource = db.query(models.Resource).filter(
            models.Resource.id == task.assigned_resource_id
        ).first()
        matching_score = calculate_matching_score(resource, task)
        if matching_score < 50:
            risk += (50 - matching_score)
    
    return min(risk, 100)
```

---

### 2. **Auto Task Assignment** 🤖
เมื่อสร้าง Task ใหม่ ให้ AI แนะนำคน Top 3:
```python
@app.post("/tasks/auto-assign/{task_id}")
async def auto_assign_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    resources = db.query(models.Resource).filter(models.Resource.is_active == True).all()
    
    # Calculate scores for all
    scores = []
    for resource in resources:
        score = calculate_matching_score(resource, task)
        scores.append({
            "resource_id": resource.id,
            "nickname": resource.nickname,
            "score": score
        })
    
    # Sort and return top 3
    scores.sort(key=lambda x: x["score"], reverse=True)
    return {"suggestions": scores[:3]}
```

---

### 3. **Smart Alerts** 🔔
แจ้งเตือนอัตโนมัติ:
- Task ที่ไม่อัพเดทเกิน 3 วัน
- Task ที่ progress < 50% และเหลือเวลา < 7 วัน
- Resource ที่มีงานเกิน 10 tasks

---

## 🔐 Phase 5: Authentication & Multi-User

### 1. **User Authentication**
```bash
pip install python-jose passlib bcrypt
```

**Features:**
- Login/Logout
- Password hashing
- JWT tokens
- Session management

---

### 2. **Role-Based Access Control (RBAC)**
Roles:
- **Admin** - ทุกอย่าง
- **PM** - จัดการโปรเจกต์ของตัวเอง
- **Resource** - อัพเดทงานของตัวเอง
- **Viewer** - ดูอย่างเดียว

---

### 3. **Activity Log**
บันทึกทุก action:
- Who did what when
- Change history
- Audit trail

---

## 📊 Phase 6: Analytics & Reports

### 1. **Dashboard Analytics**
- Total Projects (Active/Complete)
- Total Tasks (By Status)
- Average Progress
- Resource Utilization %
- Trend Charts (Last 30 days)

---

### 2. **Custom Reports**
- Resource Performance Report
- Project Health Report
- Time Tracking Report
- Risk Analysis Report

---

### 3. **Export to PDF**
```bash
pip install weasyprint
```

แปลง HTML reports → PDF

---

## 🌐 Phase 7: Integration & Deployment

### 1. **External Integrations**
- Google Calendar
- Slack/Teams notifications
- Jira sync
- Git activity tracking

---

### 2. **Docker Deployment**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 3. **Cloud Deployment**
- AWS EC2 / Elastic Beanstalk
- Azure App Service
- Google Cloud Run
- Heroku

---

## 📝 Immediate Action Items

### วันนี้ - พรุ่งนี้
1. ✅ Test ระบบที่สร้างเสร็จแล้ว
2. ⏳ สร้าง Task Registration Page
3. ⏳ สร้าง Project Details Page

### สัปดาห์นี้
4. ⏳ สร้าง Create Project Page
5. ⏳ เพิ่ม PB Curve Chart visualization
6. ⏳ ปรับปรุง Dashboard ให้แสดงข้อมูลแบบ Real-time

### สัปดาห์หน้า
7. ⏳ สร้าง Admin Tasks Page
8. ⏳ เพิ่ม Risk Prediction logic
9. ⏳ สร้าง Resource Utilization Dashboard

---

## 🎯 Prioritized Backlog

**Must Have (Phase 2):**
- [ ] Task Registration Page
- [ ] Project Details Page
- [ ] Create Project Form Page

**Should Have (Phase 3):**
- [ ] PB Curve Chart
- [ ] Resource Utilization
- [ ] Calendar View

**Nice to Have (Phase 4+):**
- [ ] Risk Prediction
- [ ] Auto Assignment
- [ ] Gantt Chart
- [ ] Authentication
- [ ] Analytics Dashboard

---

## 💡 Quick Wins (ทำได้ทันที)

### 1. เพิ่ม Navigation Links
อัพเดทไฟล์ HTML ทั้ง 3 ให้ link ไปหา:
```html
<a href="/projects/create">+ Create Project</a>
<a href="/tasks/create">+ Add Task</a>
```

### 2. เพิ่ม Favicon
```html
<link rel="icon" href="/static/favicon.ico">
```

### 3. เพิ่ม Loading States
```javascript
<div id="loading" class="hidden">Loading...</div>
```

### 4. เพิ่ม Toast Notifications
ใช้ SweetAlert2:
```html
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
```

---

## 📚 Resources สำหรับเรียนรู้

### Frontend
- Tailwind CSS: https://tailwindcss.com/docs
- Chart.js: https://www.chartjs.org/
- Alpine.js (Optional): https://alpinejs.dev/

### Backend
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Jinja2: https://jinja.palletsprojects.com/

### UI/UX
- Tailwind UI Components: https://tailwindui.com/
- Heroicons: https://heroicons.com/
- Coolors (Color Palettes): https://coolors.co/

---

## 🤝 How to Use This Roadmap

1. **เลือก Phase** ที่ต้องการทำ
2. **Copy Copilot Prompt** ไปใช้
3. **สร้างไฟล์** ตามที่แนะนำ
4. **Test** แต่ละ feature
5. **Update** roadmap นี้

---

**Current Version:** 1.1.0  
**Target Version:** 2.0.0 (Complete CRUD + Charts)  
**Timeline:** 2-4 weeks

**Happy Coding! 🚀**

