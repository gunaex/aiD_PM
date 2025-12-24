import sqlite3
import os

DB_FILE = "pm_system.db"

def fix_database():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("Checking 'projects' table schema...")
        cursor.execute("PRAGMA table_info(projects)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "progress" not in columns:
            print("Adding missing column 'progress' to 'projects' table...")
            cursor.execute("ALTER TABLE projects ADD COLUMN progress FLOAT DEFAULT 0.0")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column 'progress' already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
