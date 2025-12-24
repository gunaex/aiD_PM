"""
Migration script to add phase_id column to tasks table
"""
import sqlite3
import os

# Database path
DB_PATH = "pm_system.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'phase_id' in columns:
            print("✅ Column 'phase_id' already exists in tasks table")
        else:
            # Add phase_id column
            cursor.execute("""
                ALTER TABLE tasks 
                ADD COLUMN phase_id INTEGER REFERENCES project_phases(id)
            """)
            conn.commit()
            print("✅ Successfully added 'phase_id' column to tasks table")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting migration: Add phase_id to tasks...")
    migrate()
    print("Migration complete!")
