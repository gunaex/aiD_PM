import sqlite3
import os

DB_FILE = "pm_system.db"

def fix_phase_recovery():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("Checking 'project_phases' table schema...")
        cursor.execute("PRAGMA table_info(project_phases)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "is_recovery_mode" not in columns:
            print("Adding 'is_recovery_mode' to 'project_phases'...")
            cursor.execute("ALTER TABLE project_phases ADD COLUMN is_recovery_mode BOOLEAN DEFAULT 0")
            print("Column 'is_recovery_mode' added.")
        else:
            print("Column 'is_recovery_mode' already exists.")
            
        conn.commit()
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_phase_recovery()
