# pythonfullstack/database/init_db.py
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "library.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# -----------------------------
# CREATE BOOKS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_name TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT,
    category TEXT NOT NULL,
    date_added TEXT NOT NULL
)
""")

# -----------------------------
# CREATE USERS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    roll_no TEXT NOT NULL,
    department TEXT NOT NULL,
    library_id TEXT NOT NULL
)
""")

# -----------------------------
# CREATE ISSUED BOOKS TABLE
# -----------------------------

cur.execute("""
CREATE TABLE issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_name TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

""")




# -----------------------------
# INSERT SAMPLE BOOKS
# -----------------------------
cur.execute("SELECT COUNT(*) FROM books")
if cur.fetchone()[0] == 0:
    current_date = datetime.now().strftime("%d-%m-%Y")

    sample_books = [
        # Python
        ('Learning Python', 'Mark Lutz', '111', 'Python', current_date),
        ('Fluent Python', 'Luciano Ramalho', '112', 'Python', current_date),
        ('Python Tricks', 'Dan Bader', '113', 'Python', current_date),
        ('Effective Python', 'Brett Slatkin', '114', 'Python', current_date),
        ('Automate the Boring Stuff', 'Al Sweigart', '115', 'Python', current_date),

        # AI
        ('Artificial Intelligence', 'Stuart Russell', '201', 'AI', current_date),
        ('Deep Learning', 'Ian Goodfellow', '202', 'AI', current_date),
        ('Hands-On Machine Learning', 'Aurélien Géron', '203', 'AI', current_date),
        ('Pattern Recognition', 'Christopher Bishop', '204', 'AI', current_date),
        ('Probabilistic Machine Learning', 'Kevin Murphy', '205', 'AI', current_date),

        # ML
        ('Machine Learning', 'Tom M. Mitchell', '301', 'ML', current_date),
        ('Introduction to ML', 'Ethem Alpaydin', '302', 'ML', current_date),
        ('Basic Knowledge about ML', 'Kevin', '303', 'ML', current_date),
        ('Use of ML', 'Andreas', '304', 'ML', current_date),
        ('Real Life Application of ML', 'M. Bishop', '305', 'ML', current_date),

        # C++
        ('The C++ Programming Language', 'Bjarne Stroustrup', '401', 'C++', current_date),
        ('Effective C++', 'Scott Meyers', '402', 'C++', current_date),
        ('C++ Primer', 'Stanley Lippman', '403', 'C++', current_date),
        ('Inside the C++ Object Model', 'Andrew Koenig', '404', 'C++', current_date),
        ('Basic C++', 'Herbert Schildt', '405', 'C++', current_date),

        # C
        ('The C Programming Language', 'Dennis Ritchie', '501', 'C', current_date),
        ('Intro to C', 'Brian Kernighan', '502', 'C', current_date),
        ('Basic Knowledge about C', 'Herman', '503', 'C', current_date),
        ('Effective C', 'K.N. King', '504', 'C', current_date),
        ('Program Fundamentals', 'Tom', '505', 'C', current_date),
    ]

    cur.executemany(
        "INSERT INTO books (book_name, author, isbn, category, date_added) VALUES (?, ?, ?, ?, ?)",
        sample_books
    )

conn.commit()
conn.close()
print("✅ Database initialized successfully at:", DB_PATH)



