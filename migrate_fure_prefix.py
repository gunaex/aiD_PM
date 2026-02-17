from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import models
import os

# Database path
DB_PATH = "sqlite:///pm_system.db"
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
db = Session()

def migrate_prefixes():
    print("Starting prefix migration from FUNC- to FURE-...")
    try:
        functions = db.query(models.ProjectFunction).all()
        count = 0
        
        for f in functions:
            if f.function_code and f.function_code.startswith("FUNC-"):
                old_code = f.function_code
                new_code = old_code.replace("FUNC-", "FURE-")
                f.function_code = new_code
                print(f"Updated: {old_code} -> {new_code}")
                count += 1
                
        db.commit()
        print(f"Migration completed. {count} functions updated.")
    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    migrate_prefixes()
