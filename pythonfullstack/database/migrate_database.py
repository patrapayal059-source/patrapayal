# pythonfullstack/database/migrate_database.py
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "library.db")

def migrate_database():
    """Add date_added column to existing books table"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        # Check if date_added column exists
        cur.execute("PRAGMA table_info(books)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'date_added' not in columns:
            print("Adding date_added column...")
            
            # Add the column with default value
            current_date = datetime.now().strftime("%d-%m-%Y")
            cur.execute(f"ALTER TABLE books ADD COLUMN date_added TEXT DEFAULT '{current_date}'")
            
            # Update all existing records with current date
            cur.execute(f"UPDATE books SET date_added = '{current_date}' WHERE date_added IS NULL")
            
            conn.commit()
            print(f"✅ Successfully added date_added column to books table")
            print(f"✅ Updated all existing books with date: {current_date}")
        else:
            print("✅ date_added column already exists")
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()