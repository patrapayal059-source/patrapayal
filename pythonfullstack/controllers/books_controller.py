from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.book_service import add_book, get_all_books, search_books, delete_book, get_books_by_category ,get_db

books_bp = Blueprint("books", __name__, url_prefix="/books")

# Categories list
CATEGORIES = ["Python", "AI", "ML", "C++", "C"]
@books_bp.route("/category/<category>")
def category_books(category):
    if category not in CATEGORIES:
        flash("Unknown category", "error")
        return redirect(url_for("books.books"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE category = ? ORDER BY date_added DESC",
        (category,)
    )
    books = cursor.fetchall()
    conn.close()

    return render_template(
        "book_detail.html",
        category=category,
        books=books
    )


@books_bp.route("/")
def books():
    """Main books page showing all categories and add book form"""
    return render_template("books.html", categories=CATEGORIES)

@books_bp.route("/add", methods=["POST"])
def add_book_route():
    category = request.form.get("category")
    book_name = request.form.get("book_name")
    author = request.form.get("author")
    isbn = request.form.get("isbn")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (category, book_name, author, isbn, date_added)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (category, book_name, author, isbn))

    conn.commit()
    conn.close()

    flash("Book saved successfully!", "success")
    return redirect(url_for("books.books"))

@books_bp.route("/saved")
def saved_books():
    search = request.args.get("search", "").strip()

    conn = get_db()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
            SELECT * FROM books
            WHERE book_name LIKE ?
               OR author LIKE ?
               OR category LIKE ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM books")

    rows = cursor.fetchall()
    conn.close()

    # Group by category
    books_by_category = {}
    for row in rows:
        cat = row["category"]
        books_by_category.setdefault(cat, []).append(row)

    return render_template(
        "saved_books.html",
        books_by_category=books_by_category,
        search_query=search
    )



@books_bp.route("/delete/<int:book_id>", methods=["POST"])
def delete_book_route(book_id):
    """Delete a book from saved books"""
    try:
        delete_book(book_id)
        flash("Book deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting book: {str(e)}", "error")
    
    return redirect(url_for("books.saved_books"))

@books_bp.route("/<category>")
def book_detail(category):
    """View books for a specific category (filtered view)"""
    if category not in CATEGORIES:
        flash("Unknown category", "error")
        return redirect(url_for("books.books"))
    
    try:
        # Get books filtered by category
        category_books = get_books_by_category(category)
    except Exception as e:
        flash(f"Error loading books: {str(e)}", "error")
        category_books = []
    
    return render_template("book_detail.html", category=category, books=category_books)
