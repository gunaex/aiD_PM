"""
Initialize Complete Database for aiD_PM v1.4
Includes all tables: Projects, Tasks, Resources, Issues, Phases, Multi-Assign, etc.
"""

from database import engine, Base
import models

def init_database():
    """Create all tables in the database"""
    print("="*60)
    print("aiD_PM Database Initialization v1.4")
    print("="*60)
    
    # Drop all existing tables (careful in production!)
    print("\n1. Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("   Done!")
    
    # Create all tables
    print("\n2. Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # List created tables
    tables = [
        "projects",
        "resources",
        "tasks",
        "task_resources",  # NEW: Multi-assign
        "weekly_snapshots",
        "project_phases",  # NEW: Phase management
        "issues",  # NEW: Issue tracking
        "issue_resources",  # NEW: Multi-assign for issues
        "issue_comments",
        "issue_attachments",
        "activity_logs",
        "comments"
    ]
    
    print("\n   Tables created:")
    for table in tables:
        print(f"   - {table}")
    
    print("\n3. Database setup complete!")
    print("\n" + "="*60)
    print("Database: pm_system.db")
    print("Status: READY")
    print("="*60)
    
    print("\nNext steps:")
    print("1. Run 'python sample_data.py' to add demo data (optional)")
    print("2. Run 'uvicorn main:app --reload' to start server")
    print("3. Open http://localhost:8000")
    
    print("\nNew Features in v1.4:")
    print("- Multi-resource assignment (Tasks & Issues)")
    print("- Phase management (UR, DR, IFT, SIT, etc.)")
    print("- Enterprise issue tracking")
    print("- Backup/Restore system")
    print("- Cross-platform ready!")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Check if pm_system.db is locked (close any DB browsers)")
        print("2. Ensure models.py has no syntax errors")
        print("3. Verify database.py connection settings")

