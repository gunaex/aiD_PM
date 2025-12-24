import sqlite3
import os

DB_FILE = "pm_system.db"

def fix_activity_log():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("Checking 'activity_logs' table schema...")
        cursor.execute("PRAGMA table_info(activity_logs)")
        columns = [info[1] for info in cursor.fetchall()]
        
        # 1. Add project_id if not exists
        if "project_id" not in columns:
            print("Adding 'project_id' to 'activity_logs'...")
            cursor.execute("ALTER TABLE activity_logs ADD COLUMN project_id INTEGER REFERENCES projects(id)")
            print("Column 'project_id' added.")
        else:
            print("Column 'project_id' already exists.")

        # 2. Make task_id nullable
        # SQLite doesn't support ALTER COLUMN to change nullability easily.
        # We will have to recreate the table if we want to enforce schema strictly, 
        # but for now, just adding project_id allows us to store project logs.
        # The application code (SQLAlchemy) will treat it as nullable if we define it so.
        # However, if the DB has NOT NULL constraint, inserts will fail.
        
        # Let's check if task_id is NOT NULL
        cursor.execute("PRAGMA table_info(activity_logs)")
        # info: (cid, name, type, notnull, dflt_value, pk)
        task_id_info = next((info for info in cursor.fetchall() if info[1] == 'task_id'), None)
        
        if task_id_info and task_id_info[3] == 1: # 1 means NOT NULL
            print("Column 'task_id' is NOT NULL. Recreating table to allow NULLs...")
            
            # Rename old table
            cursor.execute("ALTER TABLE activity_logs RENAME TO activity_logs_old")
            
            # Create new table
            cursor.execute("""
                CREATE TABLE activity_logs (
                    id INTEGER PRIMARY KEY,
                    task_id INTEGER REFERENCES tasks(id),
                    project_id INTEGER REFERENCES projects(id),
                    action_type VARCHAR,
                    description VARCHAR,
                    user_name VARCHAR DEFAULT 'System',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Copy data
            print("Copying data...")
            cursor.execute("""
                INSERT INTO activity_logs (id, task_id, action_type, description, user_name, created_at)
                SELECT id, task_id, action_type, description, user_name, created_at FROM activity_logs_old
            """)
            
            # Drop old table
            cursor.execute("DROP TABLE activity_logs_old")
            print("Table recreated successfully.")
            
        conn.commit()
            
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_activity_log()
