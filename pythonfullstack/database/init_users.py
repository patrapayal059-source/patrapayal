import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("library.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT UNIQUE,
    password TEXT
)
""")

conn.execute(
    "INSERT OR IGNORE INTO users (userid, password) VALUES (?, ?)",
    ("admin", generate_password_hash("admin123"))
)

conn.commit()
conn.close()

print("✅ Users table created and admin user added")
