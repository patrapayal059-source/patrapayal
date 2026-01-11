import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
""")

# ✅ INSERT SAMPLE BOOKS
cursor.executemany(
    "INSERT INTO books (title) VALUES (?)",
    [
        ("Python Basics",),
        ("Flask Web Development",),
        ("Django for Beginners",),
        ("Data Structures",),
        ("Machine Learning",)
    ]
)

conn.commit()
conn.close()

print("Database initialized with books")
