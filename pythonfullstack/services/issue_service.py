from database.database import get_db
from datetime import datetime, timedelta

def issue_book_to_user(user_id, book_name):
    """Issue a book to a user"""
    db = get_db()
    cur = db.cursor()

    # 🔍 Check if user exists
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    if not user:
        db.close()
        return {"error": "User not found"}

    # 🔍 Check if book exists in library
    cur.execute(
        "SELECT id FROM books WHERE LOWER(book_name) = LOWER(?)",
        (book_name,)
    )
    book = cur.fetchone()

    if not book:
        db.close()
        return {"error": "This book is not present in library"}

    # 🔍 Check if user already has an unreturned book
    cur.execute(
        "SELECT id FROM issued_books WHERE user_id = ? AND return_date IS NULL",
        (user_id,)
    )
    existing_issue = cur.fetchone()
    
    if existing_issue:
        db.close()
        return {"error": "User already has an issued book that hasn't been returned"}

    # ✅ Issue the book
    issue_date = datetime.now().strftime("%Y-%m-%d")
    expected_return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO issued_books (user_id, book_name, issue_date, return_date)
        VALUES (?, ?, ?, NULL)
    """, (user_id, book_name, issue_date))

    db.commit()
    db.close()

    return {
        "issue_date": issue_date,
        "expected_return_date": expected_return_date,
        "book_name": book_name
    }


def return_book(issued_book_id):
    """Mark a book as returned"""
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


def get_user_issued_books(user_id):
    """Get all books issued to a specific user"""
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


def get_all_issued_books():
    """Get all currently issued books across all users"""
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
            issued_books.id as issued_id
        FROM issued_books
        JOIN users ON users.id = issued_books.user_id
        ORDER BY issued_books.issue_date DESC
    """)
    
    books = cur.fetchall()
    db.close()
    
    return books