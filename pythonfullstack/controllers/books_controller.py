# books_controller.py 
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.book_service import add_book, get_all_books, search_books, delete_book, get_books_by_category, get_db

books_bp = Blueprint("books", __name__, url_prefix="/books")

# Main Categories and their Subcategories
CATEGORIES = {
    "Mathematics": ["Algebra", "Geometry"],
    "Physics": ["Optics", "Gravity"],
    "Computer Science": ["C++", "C", "AI"]
}

@books_bp.route("/")
def books():
    """Main books page showing all categories"""
    return render_template("books.html", categories=CATEGORIES)

@books_bp.route("/category/<category>")
def category_view(category):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT DISTINCT subcategory
        FROM books
        WHERE category = ?
    """, (category,))

    subcategories = [row[0] for row in cur.fetchall()]

    return render_template(
        "category_view.html",
        category=category,
        subcategories=subcategories
    )

@books_bp.route("/category/<category>/<subcategory>")
def subcategory_books(category, subcategory):
    """Display books for a specific subcategory"""
    db = get_db()
    cur = db.cursor()
    
    cur.execute("""
        SELECT id, book_name, author, isbn, date_added
        FROM books
        WHERE category = ? AND subcategory = ?
        ORDER BY id DESC
    """, (category, subcategory))
    
    rows = cur.fetchall()
    db.close()
    
    # Convert rows to dictionaries for easier template access
    books = []
    for row in rows:
        books.append({
            'id': row[0],
            'book_name': row[1],
            'author': row[2],
            'isbn': row[3],
            'date_added': row[4]
        })
    
    return render_template(
        "subcategory_books.html",
        category=category,
        subcategory=subcategory,
        books=books
    )

@books_bp.route("/get-subcategories/<category>")
def get_subcategories(category):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT DISTINCT subcategory 
        FROM books 
        WHERE category = ?
    """, (category,))

    subcategories = [row[0] for row in cur.fetchall()]
    return {"subcategories": subcategories}


@books_bp.route("/add", methods=["POST"])
def add_book_route():
    category = request.form.get("category")
    subcategory = request.form.get("subcategory")
    book_name = request.form.get("book_name")
    author = request.form.get("author")
    isbn = request.form.get("isbn")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (category, subcategory, book_name, author, isbn, date_added)
        VALUES (?, ?, ?, ?, ?, DATE('now'))
    """, (category, subcategory, book_name, author, isbn))

    conn.commit()
    conn.close()

    flash("Book saved successfully!", "book")
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
               OR subcategory LIKE ?
        """, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cursor.execute("SELECT * FROM books")

    rows = cursor.fetchall()
    conn.close()

    # Group by category and subcategory
    books_by_category = {}
    for row in rows:
        cat = row["category"]
        subcat = row["subcategory"]
        key = f"{cat} - {subcat}"
        books_by_category.setdefault(key, []).append(row)

    return render_template(
        "saved_books.html",
        books_by_category=books_by_category,
        search_query=search
    )

@books_bp.route("/edit/<int:book_id>", methods=["POST"])
def edit_book(book_id):
    """
    Updates book information via AJAX request
    Receives JSON data with book_name, author, and isbn
    
    Route: POST /books/edit/<book_id>
    Content-Type: application/json
    """
    print(f"Edit route called for book_id: {book_id}")  # Debug log
    
    try:
        # Get JSON data from request
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400
        
        book_name = data.get("book_name")
        author = data.get("author")
        isbn = data.get("isbn")

        # Validate input
        if not book_name or not author:
            return jsonify({"success": False, "error": "Book name and author are required"}), 400

        db = get_db()
        cur = db.cursor()

        # Check if book exists
        cur.execute("SELECT id FROM books WHERE id = ?", (book_id,))
        if not cur.fetchone():
            db.close()
            return jsonify({"success": False, "error": "Book not found"}), 404

        # Update book in database
        cur.execute("""
            UPDATE books
            SET book_name = ?, author = ?, isbn = ?
            WHERE id = ?
        """, (book_name, author, isbn, book_id))

        db.commit()
        db.close()

        print(f"Book {book_id} updated successfully")  # Debug log

        return jsonify({
            "success": True,
            "message": "Book updated successfully"
        }), 200

    except Exception as e:
        print(f"Error in edit_book: {str(e)}")  # Debug log
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@books_bp.route("/delete/<int:book_id>", methods=["POST"])
def delete_book_route(book_id):
    """Delete a book from saved books"""
    try:
        delete_book(book_id)
        flash("Book deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting book: {str(e)}", "error")
    
    return redirect(url_for("books.saved_books"))