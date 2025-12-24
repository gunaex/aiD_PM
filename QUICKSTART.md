# 🚀 Quick Start Guide - Smart PM Control Tower

## การเริ่มต้นใช้งานภายใน 5 นาที

### ✅ Step 1: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### ✅ Step 2: สร้างข้อมูลตัวอย่าง (Optional)

```bash
python sample_data.py
```

ข้อมูลตัวอย่างที่สร้าง:
- 4 Resources (บุคลากร)
- 1 Project (Smart PM Control Tower)
- 6 Tasks (งานต่างๆ)
- 5 Weekly Snapshots (สำหรับ PB Curve)

### ✅ Step 3: รันเซิร์ฟเวอร์

```bash
python main.py
```

หรือ

```bash
uvicorn main:app --reload
```

### ✅ Step 4: เปิด API Documentation

เปิดเบราว์เซอร์ไปที่:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎯 ทดสอบ Features หลัก

### 1. ดูรายการ Resources ทั้งหมด

```bash
GET http://localhost:8000/resources
```

หรือเปิดในเบราว์เซอร์: http://localhost:8000/resources

### 2. ดูรายการ Tasks ของโปรเจกต์

```bash
GET http://localhost:8000/tasks?project_id=1
```

### 3. ทดสอบ AI Smart Matching

```bash
GET http://localhost:8000/tasks/4/suggest-resource
```

ระบบจะแนะนำบุคลากรที่เหมาะสมที่สุดสำหรับ Task ID 4 (Develop Web UI Dashboard)

### 4. ส่งออก Weekly Report

```bash
GET http://localhost:8000/export/weekly-report/1
```

หรือเปิดในเบราว์เซอร์: http://localhost:8000/export/weekly-report/1

ไฟล์จะถูกสร้างในโฟลเดอร์ `output/`

---

## 📊 ตัวอย่างการใช้งาน REST API

### สร้าง Resource ใหม่

**Request:**
```bash
POST http://localhost:8000/resources
Content-Type: application/json

{
  "full_name": "ทดสอบ ระบบ",
  "nickname": "ทด",
  "position": "Developer",
  "skills": {
    "Python": 8,
    "FastAPI": 7
  },
  "speed_score": 7,
  "quality_score": 8
}
```

### สร้างโปรเจกต์ใหม่

**Request:**
```bash
POST http://localhost:8000/projects
Content-Type: application/json

{
  "name": "New Project 2024",
  "customer": "ABC Corp",
  "methodology": "Waterfall",
  "is_recovery_mode": false,
  "budget_masked": "฿฿฿"
}
```

### อัพเดท Task Progress

**Request:**
```bash
PUT http://localhost:8000/tasks/2
Content-Type: application/json

{
  "actual_progress": 85.0
}
```

### บันทึก Weekly Snapshot

**Request:**
```bash
POST http://localhost:8000/weekly-snapshots
Content-Type: application/json

{
  "project_id": 1,
  "week_number": 6,
  "plan_acc": 75.0,
  "actual_acc": 68.0
}
```

---

## 🔍 ทดสอบผ่าน Swagger UI (แนะนำ)

1. เปิด http://localhost:8000/docs
2. คลิก "Try it out" ที่ Endpoint ที่ต้องการ
3. กรอกข้อมูลและคลิก "Execute"
4. ดูผลลัพธ์ทันที

---

## 🤖 AI Smart Matching - วิธีใช้งาน

### กรณีที่ 1: หา Resource ที่เหมาะสมสำหรับ Task

```bash
GET http://localhost:8000/tasks/{task_id}/suggest-resource
```

**ตัวอย่าง Response:**
```json
{
  "resource_id": 3,
  "full_name": "วิทยา เทคโนโลยี",
  "nickname": "วิท",
  "score": 82.5
}
```

### กรณีที่ 2: Assign Resource ให้กับ Task

```bash
PUT http://localhost:8000/tasks/4
Content-Type: application/json

{
  "assigned_resource_id": 3
}
```

---

## 📂 โครงสร้างไฟล์ที่สำคัญ

```
AID_PM/
├── main.py                    # FastAPI Application
├── models.py                  # Database Models
├── database.py                # Database Connection
├── excel_engine.py            # Excel Export Logic
├── init_db.py                 # Initialize Database
├── sample_data.py             # Create Sample Data
├── pm_system.db              # SQLite Database (auto-generated)
├── templates_excel/          # Excel Templates
│   ├── Daily_Progress_PH(PU).xls
│   └── WeeklyReport_PH(PU).xlsx
└── output/                   # Generated Reports
```

---

## 🛠️ Troubleshooting

### ปัญหา: "No module named 'xxx'"
```bash
pip install -r requirements.txt
```

### ปัญหา: "Template file not found"
ตรวจสอบว่าไฟล์ Template อยู่ในโฟลเดอร์ `templates_excel/`:
- `Daily_Progress_PH(PU).xls`
- `WeeklyReport_PH(PU).xlsx`

### ปัญหา: Port 8000 ถูกใช้งานแล้ว
```bash
# เปลี่ยน port เป็น 8001
uvicorn main:app --reload --port 8001
```

---

## 🎓 เรียนรู้เพิ่มเติม

- อ่าน `README.md` สำหรับ Architecture และ Design Philosophy
- ดู API Docs ที่ http://localhost:8000/docs
- ศึกษา `models.py` เพื่อเข้าใจ Database Schema

---

**Happy Coding! 🚀**

