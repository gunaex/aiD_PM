"""
Migration script to add project_notes table
Run this to add the notes feature to existing database
"""

from database import engine, SessionLocal
from models import Base, ProjectNote
import sqlalchemy

def migrate():
    print("🔄 Starting migration: Adding project_notes table...")
    
    # Create only the ProjectNote table
    try:
        ProjectNote.__table__.create(engine, checkfirst=True)
        print("✅ project_notes table created successfully!")
    except sqlalchemy.exc.OperationalError as e:
        if "already exists" in str(e):
            print("ℹ️  project_notes table already exists, skipping...")
        else:
            raise e
    
    print("✅ Migration completed!")

if __name__ == "__main__":
    migrate()
