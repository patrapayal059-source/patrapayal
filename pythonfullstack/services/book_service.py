from database.database import get_connection


def get_books():
    conn = get_connection()
    conn.row_factory = lambda cursor, row: {
        "id": row[0],
        "title": row[1]
    }
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return books

def get_books():
    conn = get_connection()
    data = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return data

def add_book(title):
    conn = get_connection()
    conn.execute("INSERT INTO books(title) VALUES(?)", (title,))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    conn.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
