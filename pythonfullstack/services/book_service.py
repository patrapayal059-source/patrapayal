# import sys
# import os

# # Add parent directory to sys.path to import database module
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from database.db import get_connection

# class BookService:
#     """Service class for book CRUD operations."""

#     @staticmethod
#     def list_books():
#         """Return all books ordered by id descending."""
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM books ORDER BY id DESC")
#         rows = cur.fetchall()
#         conn.close()
#         return [dict(r) for r in rows]

#     @staticmethod
#     def get_book(book_id):
#         """Return a single book by ID."""
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
#         row = cur.fetchone()
#         conn.close()
#         return dict(row) if row else None

#     @staticmethod
#     def create_book(data):
#         """Create a new book and return it."""
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(
#             "INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)",
#             (data["title"], data["author"], data["isbn"], data.get("year"))
#         )
#         conn.commit()
#         new_id = cur.lastrowid
#         conn.close()
#         return BookService.get_book(new_id)

#     @staticmethod
#     def update_book(book_id, data):
#         """Update book details and return updated book."""
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute(
#             "UPDATE books SET title=?, author=?, isbn=?, year=? WHERE id=?",
#             (data["title"], data["author"], data["isbn"], data.get("year"), book_id)
#         )
#         conn.commit()
#         conn.close()
#         return BookService.get_book(book_id)

#     @staticmethod
#     def delete_book(book_id):
#         """Delete a book. Returns True if deleted, False otherwise."""
#         conn = get_connection()
#         cur = conn.cursor()
#         cur.execute("DELETE FROM books WHERE id=?", (book_id,))
#         conn.commit()
#         deleted = cur.rowcount
#         conn.close()
#         return deleted > 0

# # Example usage (optional)
# if __name__ == "__main__":
#     # Example dictionary for creating a book
#     sample_book = {"title": "Python Basics", "author": "John Doe", "isbn": "1234567890", "year": 2025}

#     # Create a book
#     book = BookService.create_book(sample_book)
#     print("Created Book:", book)

#     # List all books
#     print("All Books:", BookService.list_books())

#     # Update the book
#     updated_data = {"title": "Python Basics Updated", "author": "Jane Doe", "isbn": "1234567890", "year": 2025}
#     updated_book = BookService.update_book(book["id"], updated_data)
#     print("Updated Book:", updated_book)

#     # Get a single book
#     print("Get Book:", BookService.get_book(book["id"]))

#     # Delete the book
#     print("Deleted:", BookService.delete_book(book["id"]))




import sys
import os

# Add project folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from database.db import get_connection
from database.db import get_connection


class BookService:
    @staticmethod
    def list_books():
        """Return all books ordered by id descending."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_book(book_id):
        """Return a single book by ID."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_book(data):
        """Create a new book and return it."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)",
                (data["title"], data["author"], data["isbn"], data.get("year"))
            )
            conn.commit()
            new_id = cur.lastrowid
            return BookService.get_book(new_id)
        finally:
            conn.close()

    @staticmethod
    def update_book(book_id, data):
        """Update book details and return updated book."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE books SET title=?, author=?, isbn=?, year=? WHERE id=?",
                (data["title"], data["author"], data["isbn"], data.get("year"), book_id)
            )
            conn.commit()
            return BookService.get_book(book_id)
        finally:
            conn.close()

    @staticmethod
    def delete_book(book_id):
        """Delete a book. Returns True if deleted, False otherwise."""
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM books WHERE id=?", (book_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()


# --- Example usage ---
if __name__ == "__main__":
    # Sample book data
    sample_book = {"title": "Python Basics", "author": "John Doe", "isbn": "1234567890", "year": 2025}

    # Create book
    book = BookService.create_book(sample_book)
    print("Created Book:", book)

    # List all books
    print("All Books:", BookService.list_books())

    # Update book
    updated_data = {"title": "Python Basics Updated", "author": "Jane Doe", "isbn": "1234567890", "year": 2025}
    updated_book = BookService.update_book(book["id"], updated_data)
    print("Updated Book:", updated_book)
    # Get single book
    print("Get Book:", BookService.get_book(book["id"]))

    # Delete book
    print("Deleted:", BookService.delete_book(book["id"]))
