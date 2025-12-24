from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# SQLite Database
DATABASE_URL = "sqlite:///./pm_system.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """สร้างตารางทั้งหมดในฐานข้อมูล"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency สำหรับ FastAPI เพื่อเข้าถึง database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

