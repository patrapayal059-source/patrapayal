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
    subcategory TEXT NOT NULL,
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
CREATE TABLE IF NOT EXISTS issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_name TEXT,
    issue_date DATE,
    return_date DATE
)
""")

# -----------------------------
# INSERT SAMPLE BOOKS
# -----------------------------
cur.execute("SELECT COUNT(*) FROM books")
if cur.fetchone()[0] == 0:
    current_date = datetime.now().strftime("%d-%m-%Y")

    sample_books = [
        # ========== MATHEMATICS - ALGEBRA ==========
        ('Algebra', 'Michael Artin', '101', 'Mathematics', 'Algebra', current_date),
        ('Abstract Algebra', 'David S. Dummit and Richard M. Foote', '102', 'Mathematics', 'Algebra', current_date),
        ('Algebra: Chapter 0', 'Paolo Aluffi', '103', 'Mathematics', 'Algebra', current_date),
        ('Elementary Algebra', 'Harold R. Jacobs', '104', 'Mathematics', 'Algebra', current_date),
        ('Linear Algebra and Its Applications', 'Gilbert Strang', '105', 'Mathematics', 'Algebra', current_date),

        # ========== MATHEMATICS - GEOMETRY ==========
        ('Euclidean and Non-Euclidean Geometries', 'Marvin J. Greenberg', '201', 'Mathematics', 'Geometry', current_date),
        ('Geometry: Euclid and Beyond', 'Robin Hartshorne', '202', 'Mathematics', 'Geometry', current_date),
        ('Introduction to Geometry', 'H. S. M. Coxeter', '203', 'Mathematics', 'Geometry', current_date),
        ('College Geometry: A Problem-Solving Approach with Applications', 'Gary Musser and Lynn Trimpe', '204', 'Mathematics', 'Geometry', current_date),
        ('Geometry Revisited', 'H. S. M. Coxeter', '205', 'Mathematics', 'Geometry', current_date),

        # ========== PHYSICS - OPTICS ==========
        ('Optics', 'Eugene Hecht', '301', 'Physics', 'Optics', current_date),
        ('Introduction to Optics', 'Frank L. Pedrotti, Leno M. Pedrotti, and Leno S. Pedrotti', '302', 'Physics', 'Optics', current_date),
        ('Principles of Optics', 'Max Born and Emil Wolf', '303', 'Physics', 'Optics', current_date),
        ('Introduction to Modern Optics', 'Grant R. Fowles', '304', 'Physics', 'Optics', current_date),
        ('Fundamentals of Photonics', 'Bahaa E. A. Saleh and Malvin Carl Teich', '305', 'Physics', 'Optics', current_date),

        # ========== PHYSICS - GRAVITY ==========
        ('Gravity: An Introduction to Einstein\'s General Relativity', 'James B. Hartle', '401', 'Physics', 'Gravity', current_date),
        ('The Ascent of Gravity: The Quest to Understand the Force that Explains Everything', 'Marcus Chown', '402', 'Physics', 'Gravity', current_date),
        ('Gravity\'s Engines: How Bubble-Blowing Black Holes Rule Galaxies, Stars, and Life in the Cosmos', 'Caleb Scharf', '403', 'Physics', 'Gravity', current_date),
        ('Gravity\'s Rainbow', 'Thomas Pynchon', '404', 'Physics', 'Gravity', current_date),
        ('Gravity: How the Weakest Force in the Universe Shaped Our Lives', 'Brian Clegg', '405', 'Physics', 'Gravity', current_date),

        # ========== COMPUTER SCIENCE - C++ ==========
        ('The C++ Programming Language', 'Bjarne Stroustrup', '501', 'Computer Science', 'C++', current_date),
        ('Effective C++', 'Scott Meyers', '502', 'Computer Science', 'C++', current_date),
        ('C++ Primer', 'Stanley Lippman', '503', 'Computer Science', 'C++', current_date),
        ('Inside the C++ Object Model', 'Andrew Koenig', '504', 'Computer Science', 'C++', current_date),
        ('Basic C++', 'Herbert Schildt', '505', 'Computer Science', 'C++', current_date),

        # ========== COMPUTER SCIENCE - C ==========
        ('The C Programming Language', 'Dennis Ritchie', '601', 'Computer Science', 'C', current_date),
        ('Intro to C', 'Brian Kernighan', '602', 'Computer Science', 'C', current_date),
        ('C Programming: A Modern Approach', 'K.N. King', '603', 'Computer Science', 'C', current_date),
        ('Programming in C', 'Stephen Kochan', '604', 'Computer Science', 'C', current_date),
        ('C: The Complete Reference', 'Herbert Schildt', '605', 'Computer Science', 'C', current_date),
                # ========== COMPUTER SCIENCE - AI ==========
        ('Artificial Intelligence', 'Stuart Russell & Peter Norvig', '701', 'Computer Science', 'AI', current_date),
        ('Deep Learning', 'Ian Goodfellow', '702', 'Computer Science', 'AI', current_date),
        ('Hands-On Machine Learning', 'Aurélien Géron', '703', 'Computer Science', 'AI', current_date),
        ('Pattern Recognition and Machine Learning', 'Christopher Bishop', '704', 'Computer Science', 'AI', current_date),
        ('Probabilistic Machine Learning', 'Kevin Murphy', '705', 'Computer Science', 'AI', current_date),


    ]

    cur.executemany(
        "INSERT INTO books (book_name, author, isbn, category, subcategory, date_added) VALUES (?, ?, ?, ?, ?, ?)",
        sample_books
    )

conn.commit()
conn.close()
print("✅ Database initialized successfully at:", DB_PATH)