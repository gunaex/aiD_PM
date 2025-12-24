"""
Script สำหรับ Initialize Database
รันไฟล์นี้เพื่อสร้างตารางในฐานข้อมูล
"""
from database import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    print("Database file: pm_system.db")
    print("\nYou can now run the server:")
    print("   python main.py")
    print("   or")
    print("   uvicorn main:app --reload")

