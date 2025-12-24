import sqlite3

def migrate_db():
    conn = sqlite3.connect('pm_system.db')
    cursor = conn.cursor()
    
    try:
        # Add 'company' column
        try:
            cursor.execute("ALTER TABLE resources ADD COLUMN company TEXT")
            print("Added 'company' column.")
        except sqlite3.OperationalError:
            print("'company' column already exists.")
            
        # Add 'comment' column
        try:
            cursor.execute("ALTER TABLE resources ADD COLUMN comment TEXT")
            print("Added 'comment' column.")
        except sqlite3.OperationalError:
            print("'comment' column already exists.")
            
        # Add 'skills' column
        try:
            cursor.execute("ALTER TABLE resources ADD COLUMN skills TEXT")
            print("Added 'skills' column.")
        except sqlite3.OperationalError:
            print("'skills' column already exists.")
            
        conn.commit()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_db()
