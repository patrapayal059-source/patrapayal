from werkzeug.security import generate_password_hash
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid TEXT UNIQUE,
    password TEXT
)
""")

# Insert admin user
cursor.execute(
    "INSERT OR IGNORE INTO users (userid, password) VALUES (?, ?)",
    ("admin", generate_password_hash("admin123"))
)

# Commit and close
conn.commit()

# Fetch and display all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(user)

conn.close()
print("Admin user added (if not exists) and all users displayed!")
