from database.database import get_db
from datetime import datetime, timedelta

def issue_book_to_user(user_id, book_name):
    db = get_db()
    cur = db.cursor()

    # 🔍 check book exists
    cur.execute(
        "SELECT id FROM books WHERE LOWER(book_name) = LOWER(?)",
        (book_name,)
    )
    book = cur.fetchone()

    if not book:
        db.close()
        return {"error": "Book not present"}

    issue_date = datetime.now().strftime("%Y-%m-%d")
    return_date = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

    cur.execute("""
        INSERT INTO issued_books (user_id, book_name, issue_date, return_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, book_name, issue_date, return_date))

    db.commit()
    db.close()

    return {
        "issue_date": issue_date,
        "return_date": return_date
    }


