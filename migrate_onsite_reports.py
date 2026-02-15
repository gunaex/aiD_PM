"""
Migration script to add CompanyProfile and OnsiteReport tables
Run this once to update the database schema
"""
from database import engine
import models

def migrate():
    """Create new tables for onsite reports feature"""
    print("Starting migration: Adding company_profiles and onsite_reports tables...")
    
    try:
        # Create all tables (will only create missing ones)
        models.Base.metadata.create_all(bind=engine)
        print("✓ Migration completed successfully!")
        print("  - company_profiles table created")
        print("  - onsite_reports table created")
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
