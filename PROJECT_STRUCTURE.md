# 📁 Project Structure - Smart PM Control Tower

## โครงสร้างไฟล์ทั้งหมด

```
D:\git\aiD_PM\
│
├── 📄 main.py                          # FastAPI Application (Core)
│   ├── API Endpoints (CRUD)
│   ├── AI Smart Matching Logic
│   └── Excel Export Triggers
│
├── 📄 models.py                        # Database Models (SQLAlchemy)
│   ├── Resource (บุคลากร)
│   ├── Project (โปรเจกต์)
│   ├── Task (งาน)
│   └── WeeklySnapshot (PB Curve)
│
├── 📄 database.py                      # Database Configuration
│   ├── SQLite Connection
│   ├── Session Management
│   └── init_db() function
│
├── 📄 excel_engine.py                  # Excel Export Logic
│   ├── export_weekly_report()
│   └── export_daily_progress()
│
├── 📄 init_db.py                       # Database Initialization Script
│   └── สร้างตารางในฐานข้อมูล
│
├── 📄 sample_data.py                   # Sample Data Generator
│   ├── สร้าง Resources ตัวอย่าง
│   ├── สร้าง Project ตัวอย่าง
│   ├── สร้าง Tasks ตัวอย่าง
│   └── สร้าง Weekly Snapshots ตัวอย่าง
│
├── 📄 requirements.txt                 # Python Dependencies
│   ├── fastapi==0.127.0
│   ├── uvicorn==0.40.0
│   ├── sqlalchemy==2.0.45
│   ├── openpyxl==3.1.5
│   ├── pandas==2.3.3
│   ├── jinja2==3.1.6
│   └── python-multipart==0.0.21
│
├── 📄 .gitignore                       # Git Ignore Rules
│   ├── Ignore .venv/
│   ├── Ignore *.db
│   ├── Ignore output/
│   └── Ignore __pycache__/
│
├── 📄 README.md                        # Project Documentation (Main)
│   ├── Features Overview
│   ├── Architecture
│   ├── Quick Start Guide
│   ├── API Endpoints
│   └── Usage Examples
│
├── 📄 QUICKSTART.md                    # Quick Start Guide (5 minutes)
│   ├── Step-by-step Setup
│   ├── Testing Features
│   └── API Examples
│
├── 📄 COPILOT_CONTEXT.md              # Context for Copilot Chat
│   ├── Architecture Details
│   ├── AI Logic Explanation
│   ├── Database Schema
│   └── Development Guidelines
│
├── 📄 PROJECT_STRUCTURE.md            # This File
│   └── Complete Project Structure
│
├── 🗄️ pm_system.db                    # SQLite Database (Auto-generated)
│   └── Contains all project data
│
├── 📁 .venv\                          # Virtual Environment
│   └── Python packages (isolated)
│
├── 📁 templates_excel\                # Excel Templates (Read-only)
│   ├── Daily_Progress_PH(PU).xls     # Daily Report Template
│   └── WeeklyReport_PH(PU).xlsx      # Weekly Report Template
│
├── 📁 output\                         # Generated Excel Reports
│   ├── WeeklyReport_Project_1_*.xlsx
│   └── DailyProgress_Project_1_*.xls
│
└── 📁 __pycache__\                    # Python Cache (Auto-generated)
    └── Compiled Python files
```

---

## 📊 File Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py (Core)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Routes                                      │  │
│  │  - Resources CRUD                                    │  │
│  │  - Projects CRUD                                     │  │
│  │  - Tasks CRUD                                        │  │
│  │  - AI Smart Matching                                 │  │
│  │  - Excel Export Endpoints                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ imports
                           ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
│  models.py   │◄───│ database.py  │◄───│ excel_engine.py  │
│              │    │              │    │                  │
│ - Resource   │    │ - Engine     │    │ - Weekly Report  │
│ - Project    │    │ - Session    │    │ - Daily Progress │
│ - Task       │    │ - init_db()  │    │                  │
│ - Snapshot   │    │              │    │                  │
└──────────────┘    └──────────────┘    └──────────────────┘
       │                   │                      │
       │                   │                      │
       ▼                   ▼                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    pm_system.db                             │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  ┌────────────────┐ │
│  │resources │  │ projects │  │tasks │  │weekly_snapshots│ │
│  └──────────┘  └──────────┘  └──────┘  └────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ reads from
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    excel_engine.py                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Loads Templates                                     │  │
│  │  ┌────────────────┐    ┌──────────────────────┐     │  │
│  │  │ Daily_Progress │    │ WeeklyReport_PH.xlsx │     │  │
│  │  └────────────────┘    └──────────────────────┘     │  │
│  │                                                      │  │
│  │  Fills Data → Saves to output/                      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Files Explained

### 1. **main.py** (500+ lines)
**Purpose:** หัวใจของระบบ - FastAPI Application

**Key Functions:**
- `create_resource()` - สร้างบุคลากร
- `create_project()` - สร้างโปรเจกต์
- `create_task()` - สร้างงาน
- `calculate_matching_score()` - 🤖 AI Logic
- `suggest_best_resource()` - แนะนำบุคลากร
- `export_weekly_report_endpoint()` - ส่งออก Excel

**Dependencies:**
- models.py (Database Models)
- database.py (Database Connection)
- excel_engine.py (Excel Export)

---

### 2. **models.py** (50 lines)
**Purpose:** โครงสร้างฐานข้อมูล (SQLAlchemy ORM)

**Tables:**
- `resources` - บุคลากร (8 columns)
- `projects` - โปรเจกต์ (7 columns)
- `tasks` - งาน (11 columns)
- `weekly_snapshots` - สำหรับ PB Curve (5 columns)

**Special Fields:**
- `skills` (JSON) - เก็บ skill matrix
- `ai_risk_score` (Float) - Hidden intelligence
- `weight_score` (Float) - Value-based tracking

---

### 3. **database.py** (20 lines)
**Purpose:** จัดการการเชื่อมต่อฐานข้อมูล

**Key Components:**
- `DATABASE_URL` - SQLite connection string
- `engine` - SQLAlchemy engine
- `SessionLocal` - Session factory
- `init_db()` - สร้างตารางทั้งหมด
- `get_db()` - Dependency injection สำหรับ FastAPI

---

### 4. **excel_engine.py** (60 lines)
**Purpose:** Logic การส่งออก Excel

**Functions:**
- `export_weekly_report()` - สร้าง Weekly Report
  - โหลด Template
  - Query WeeklySnapshots
  - เติมข้อมูลใน "PB Curve" sheet (row 41+)
  - Save ไฟล์ใหม่

- `export_daily_progress()` - สร้าง Daily Progress
  - โหลด Template
  - Query Tasks
  - เติมข้อมูล
  - Save ไฟล์ใหม่

---

### 5. **init_db.py** (15 lines)
**Purpose:** Script สำหรับสร้างฐานข้อมูล

**Usage:**
```bash
python init_db.py
```

**Output:**
- สร้างไฟล์ `pm_system.db`
- สร้างตารางทั้งหมด (resources, projects, tasks, weekly_snapshots)

---

### 6. **sample_data.py** (120 lines)
**Purpose:** สร้างข้อมูลตัวอย่างสำหรับทดสอบ

**Creates:**
- 4 Resources (สมชาย, สมหญิง, วิทยา, อนันต์)
- 1 Project (Smart PM Control Tower)
- 6 Tasks (งานต่างๆ)
- 5 Weekly Snapshots (Week 1-5)

**Usage:**
```bash
python sample_data.py
```

---

## 📚 Documentation Files

### README.md
- Overview ของโปรเจกต์
- Features หลัก
- Architecture diagram
- API Endpoints
- Usage examples
- Tech stack

### QUICKSTART.md
- Quick start guide (5 นาที)
- Step-by-step setup
- Testing features
- API examples
- Troubleshooting

### COPILOT_CONTEXT.md
- Context สำหรับ Copilot Chat
- Architecture details
- AI logic explanation
- Database schema
- Development guidelines

### PROJECT_STRUCTURE.md (This file)
- โครงสร้างไฟล์ทั้งหมด
- File relationships
- Core files explained

---

## 🔄 Data Flow

```
1. User Request
   ↓
2. FastAPI Endpoint (main.py)
   ↓
3. Database Query (database.py + models.py)
   ↓
4. Business Logic (main.py)
   ├─→ AI Matching (calculate_matching_score)
   └─→ Excel Export (excel_engine.py)
   ↓
5. Response to User
   ├─→ JSON (API Response)
   └─→ File Download (Excel)
```

---

## 🚀 Startup Sequence

```
1. Activate Virtual Environment
   .venv\Scripts\activate

2. Initialize Database (if first time)
   python init_db.py

3. Create Sample Data (optional)
   python sample_data.py

4. Run Server
   python main.py
   or
   uvicorn main:app --reload

5. Access API
   http://localhost:8000/docs
```

---

## 📊 Database Tables Relationship

```
┌──────────────┐
│  resources   │
│  (บุคลากร)   │
└──────┬───────┘
       │
       │ assigned_resource_id (FK)
       │
       ▼
┌──────────────┐        ┌──────────────────┐
│   projects   │◄───────│      tasks       │
│  (โปรเจกต์)  │        │      (งาน)       │
└──────┬───────┘        └──────────────────┘
       │                 project_id (FK)
       │
       │ project_id (FK)
       │
       ▼
┌──────────────────┐
│ weekly_snapshots │
│   (PB Curve)     │
└──────────────────┘
```

---

## 🎨 File Size Summary

| File | Lines | Purpose |
|------|-------|---------|
| main.py | ~500 | FastAPI Application |
| models.py | ~50 | Database Models |
| database.py | ~20 | Database Connection |
| excel_engine.py | ~60 | Excel Export |
| init_db.py | ~15 | DB Initialization |
| sample_data.py | ~120 | Sample Data |
| requirements.txt | ~7 | Dependencies |
| README.md | ~250 | Main Documentation |
| QUICKSTART.md | ~200 | Quick Start Guide |
| COPILOT_CONTEXT.md | ~300 | Copilot Context |

**Total:** ~1,500+ lines of code and documentation

---

## ✅ Foundation Complete

ระบบ "ฐานราก" ของโปรเจกต์ AID_PM สร้างเสร็จสมบูรณ์แล้ว!

**Ready for:**
- ✅ API Development
- ✅ Database Operations
- ✅ AI Smart Matching
- ✅ Excel Export
- ⏳ Frontend Development (Next Phase)

---

**Last Updated:** 2024-12-24  
**Version:** 1.0.0  
**Status:** Foundation Complete 🎉

