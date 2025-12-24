# 🚀 Smart PM Control Tower (AID_PM)

ระบบจัดการโปรเจกต์อัจฉริยะที่ผสานความสามารถของ AI เข้ากับการบริหารโปรเจกต์แบบมืออาชีพ

## ✨ Features

### 🎯 Core Functions
- **Project Management**: จัดการโปรเจกต์แบบหลากหลาย Methodology (Waterfall, Scrum, Kanban)
- **Resource Management**: บริหารจัดการทีมงานพร้อม Skill Matrix
- **Task Tracking**: ติดตามงานแบบ Value-Based (Weight Score)
- **AI Smart Matching**: แนะนำบุคลากรที่เหมาะสมสำหรับงานแต่ละชิ้น (Hidden Intelligence)
- **PB Curve Analysis**: วิเคราะห์ความก้าวหน้าของโปรเจกต์แบบ Plan vs Actual

### 📊 Reporting
- **Daily Progress Report**: รายงานประชุมภายในทีม
- **Weekly Report**: รายงานลูกค้าพร้อม PB Curve
- รองรับ Excel Templates ที่มีอยู่แล้ว

## 🏗️ Architecture

```
AID_PM/
├── models.py              # Database Models (SQLAlchemy)
├── database.py            # Database Connection & Setup
├── excel_engine.py        # Excel Export Logic
├── main.py                # FastAPI Application
├── requirements.txt       # Python Dependencies
├── pm_system.db          # SQLite Database (auto-generated)
├── templates_excel/       # Excel Templates
│   ├── Daily_Progress_PH(PU).xls
│   └── WeeklyReport_PH(PU).xlsx
└── output/                # Generated Reports (auto-created)
```

## 🚀 Quick Start

### 1. สร้าง Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 4. รันเซิร์ฟเวอร์
```bash
python main.py
```

หรือ

```bash
uvicorn main:app --reload
```

### 5. เปิดเบราว์เซอร์
- **API Docs (Swagger UI)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 📡 API Endpoints

### Resources (บุคลากร)
- `POST /resources` - สร้างบุคลากรใหม่
- `GET /resources` - ดึงรายการบุคลากรทั้งหมด
- `GET /resources/{id}` - ดึงข้อมูลบุคลากรตาม ID
- `PUT /resources/{id}` - อัพเดทข้อมูลบุคลากร
- `DELETE /resources/{id}` - ลบบุคลากร (Soft Delete)

### Projects (โปรเจกต์)
- `POST /projects` - สร้างโปรเจกต์ใหม่
- `GET /projects` - ดึงรายการโปรเจกต์ทั้งหมด
- `GET /projects/{id}` - ดึงข้อมูลโปรเจกต์ตาม ID
- `PUT /projects/{id}` - อัพเดทข้อมูลโปรเจกต์

### Tasks (งาน)
- `POST /tasks` - สร้างงานใหม่
- `GET /tasks?project_id={id}` - ดึงรายการงานของโปรเจกต์
- `GET /tasks/{id}` - ดึงข้อมูลงานตาม ID
- `PUT /tasks/{id}` - อัพเดทความคืบหน้าหรือมอบหมายบุคลากร
- `GET /tasks/{id}/suggest-resource` - 🤖 แนะนำบุคลากรที่เหมาะสม (AI)

### Weekly Snapshots (สำหรับ PB Curve)
- `POST /weekly-snapshots` - บันทึก Snapshot รายสัปดาห์
- `GET /weekly-snapshots?project_id={id}` - ดึงข้อมูล Snapshots

### Excel Reports
- `GET /export/weekly-report/{project_id}` - ส่งออก Weekly Report
- `GET /export/daily-progress/{project_id}` - ส่งออก Daily Progress

## 💡 Usage Examples

### สร้าง Resource
```bash
curl -X POST "http://localhost:8000/resources" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "สมชาย ใจดี",
    "nickname": "ชาย",
    "position": "Senior Developer",
    "skills": {
      "Python": 9,
      "SQL": 8,
      "FastAPI": 8
    },
    "speed_score": 8,
    "quality_score": 9
  }'
```

### สร้าง Project
```bash
curl -X POST "http://localhost:8000/projects" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smart PM System",
    "customer": "ABC Company",
    "methodology": "Scrum",
    "is_recovery_mode": false,
    "budget_masked": "฿฿฿"
  }'
```

### สร้าง Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "task_name": "Develop API Endpoints",
    "task_type": "Dev",
    "weight_score": 5.0,
    "planned_start": "2024-01-01",
    "planned_end": "2024-01-15"
  }'
```

### ขอคำแนะนำ Resource (AI)
```bash
curl -X GET "http://localhost:8000/tasks/1/suggest-resource"
```

## 🎨 Design Philosophy

- **Professional BI Style**: Dark/Slate theme พร้อม Tailwind CSS
- **No AI Icons**: ซ่อนความฉลาดของ AI ไว้เบื้องหลัง
- **Value-Based Tracking**: คำนวณความคืบหน้าจาก Weight Score
- **Hidden Intelligence**: AI ทำงานแบบโปร่งใส ไม่รบกวนผู้ใช้

## 🔐 Database Schema

### Resources (บุคลากร)
- Skills as JSON
- Speed Score (1-10)
- Quality Score (1-10)

### Projects (โปรเจกต์)
- Multiple Methodologies
- Recovery Mode Support
- Budget Masking

### Tasks (งาน)
- Value-Based Weight Score
- AI Risk Score (Hidden)
- Resource Assignment

### Weekly Snapshots
- Plan Accumulation
- Actual Accumulation
- For PB Curve Analysis

## 🤖 AI Smart Matching

ระบบจะแนะนำบุคลากรที่เหมาะสมโดยพิจารณาจาก:
1. **Skills Match**: ความตรงกันระหว่าง Task Type กับ Resource Skills
2. **Speed Score**: ความเร็วในการทำงาน
3. **Quality Score**: คุณภาพของงาน

Score รวม 0-100 คะแนน (ซ่อนไว้จากผู้ใช้)

## 📝 Development Roadmap

- [x] Database Models
- [x] FastAPI Backend
- [x] CRUD Operations
- [x] AI Smart Matching
- [x] Excel Export Engine
- [ ] Web UI (Frontend)
- [ ] Real-time Dashboard
- [ ] Advanced Analytics

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.127.0
- **Database**: SQLAlchemy 2.0.45 + SQLite
- **Excel**: openpyxl 3.1.5
- **Data Processing**: pandas 2.3.3
- **Server**: Uvicorn 0.40.0

## 📄 License

Proprietary - For internal use only

---

**Developed with ❤️ for Smart Project Management**

