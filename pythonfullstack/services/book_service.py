
from database.database import get_db
from datetime import datetime

def add_book(book_name, author, isbn, category):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO books (book_name, author, isbn, category, date_added)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (book_name, author, isbn, category))

    conn.commit()
    conn.close()


def get_all_books():
    """Get all saved books"""
    db = get_db()
    cur = db.cursor()
    
    try:
        cur.execute("SELECT id, book_name, author, isbn, date_added FROM books ORDER BY id DESC")
    except:
        # Fallback if date_added column doesn't exist
        cur.execute("SELECT id, book_name, author, isbn, '' as date_added FROM books ORDER BY id DESC")
    
    books = cur.fetchall()
    db.close()
    return books

def search_books(query):
    """Search books by name, author, or date"""
    db = get_db()
    cur = db.cursor()
    
    search_pattern = f"%{query}%"
    
    try:
        cur.execute("""
            SELECT id, book_name, author, isbn, date_added 
            FROM books 
            WHERE book_name LIKE ? OR author LIKE ? OR date_added LIKE ?
            ORDER BY id DESC
        """, (search_pattern, search_pattern, search_pattern))
    except:
        # Fallback if date_added column doesn't exist
        cur.execute("""
            SELECT id, book_name, author, isbn, '' as date_added 
            FROM books 
            WHERE book_name LIKE ? OR author LIKE ?
            ORDER BY id DESC
        """, (search_pattern, search_pattern))
    
    books = cur.fetchall()
    db.close()
    return books

def delete_book(book_id):
    """Delete a book by ID"""
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    db.close()

def get_books_by_category(category):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM books WHERE category = ?",
        (category,)
    )
    books = cur.fetchall()
    conn.close()
    return books
