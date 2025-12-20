import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "library.db"
import sqlite3

DB_FILE = "library.db"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Optional: return dict-like rows
    return conn

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not DB_PATH.exists():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            year INTEGER
        )
        """)
        conn.commit()
        conn.close()
        print("✅ Database created successfully!")
    else:
        print("✔️ Database already exists. Skipping creation.")

init_db()
