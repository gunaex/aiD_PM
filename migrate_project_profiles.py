"""
Migration script to update CompanyProfile to be project-specific
Run this to add project_id to existing company_profiles table
"""
from database import engine, SessionLocal
import models
from sqlalchemy import text

def migrate():
    """Update company_profiles to be project-specific"""
    print("Starting migration: Making company profiles project-specific...")
    
    db = SessionLocal()
    
    try:
        # Drop the old table and recreate with new schema
        print("  - Dropping old company_profiles table...")
        db.execute(text("DROP TABLE IF EXISTS company_profiles"))
        db.commit()
        
        # Recreate with new schema
        print("  - Creating new company_profiles table with project_id...")
        models.Base.metadata.create_all(bind=engine, tables=[models.CompanyProfile.__table__])
        
        print("✓ Migration completed successfully!")
        print("  - company_profiles table updated with project_id")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate()
