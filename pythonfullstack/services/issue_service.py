from database.database import get_db
from datetime import datetime


# ================= ISSUE BOOK =================
def issue_book_to_user(user_id, book_name):
    db = get_db()
    cur = db.cursor()

    # ✅ Normalize input
    book_name = book_name.strip().lower()

    # 🔍 Check user exists
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cur.fetchone():
        db.close()
        return {"error": "User not found"}

    # 🔍 STRICT: Check book exists in library
    cur.execute("""
        SELECT id
        FROM books
        WHERE LOWER(TRIM(book_name)) = ?
    """, (book_name,))
    book = cur.fetchone()

    if not book:
        db.close()
        return {"error": "This book is not present in the library"}

    # 🔍 Check if book already issued (any user)
    cur.execute("""
        SELECT id
        FROM issued_books
        WHERE LOWER(TRIM(book_name)) = ?
          AND return_date IS NULL
    """, (book_name,))
    if cur.fetchone():
        db.close()
        return {"error": "This book is already issued to another user"}

    # 🔍 Check if user already has a book
    cur.execute("""
        SELECT id
        FROM issued_books
        WHERE user_id = ?
          AND return_date IS NULL
    """, (user_id,))
    if cur.fetchone():
        db.close()
        return {"error": "User already has an issued book"}

    # ✅ Issue book
    issue_date = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO issued_books (user_id, book_name, issue_date, return_date)
        VALUES (?, ?, ?, NULL)
    """, (user_id, book_name.upper(), issue_date))

    db.commit()
    db.close()

    return {
        "book_name": book_name.upper(),
        "issue_date": issue_date
    }


# ================= RETURN BOOK =================
def return_book(issued_book_id):
    db = get_db()
    cur = db.cursor()

    return_date = datetime.now().strftime("%Y-%m-%d")

    cur.execute("""
        UPDATE issued_books
        SET return_date = ?
        WHERE id = ?
    """, (return_date, issued_book_id))

    db.commit()
    db.close()

    return {"success": True, "return_date": return_date}


# ================= USER ISSUED BOOKS =================
def get_user_issued_books(user_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, book_name, issue_date, return_date
        FROM issued_books
        WHERE user_id = ?
        ORDER BY issue_date DESC
    """, (user_id,))

    books = cur.fetchall()
    db.close()
    return books


# ================= ALL ISSUED BOOKS =================
def get_all_issued_books():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT 
            users.username,
            users.roll_no,
            users.department,
            issued_books.book_name,
            issued_books.issue_date,
            issued_books.return_date,
            issued_books.id AS issued_id
        FROM issued_books
        JOIN users ON users.id = issued_books.user_id
        ORDER BY issued_books.issue_date DESC
    """)

    books = cur.fetchall()
    db.close()
    return books
