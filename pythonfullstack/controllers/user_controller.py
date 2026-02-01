from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.database import get_db

users_bp = Blueprint("users", __name__, url_prefix="/users")
LIBRARY_ID = "LIB-2026"

# ================= PROFILE =================
@users_bp.route("/", methods=["GET"])
def profile():
    db = get_db()
    cur = db.cursor()

    # Get all users with their most recent issued book (if any)
    cur.execute("""
        SELECT 
            users.id,
            users.username,
            users.roll_no,
            users.department,
            issued_books.book_name,
            issued_books.issue_date,
            issued_books.return_date
        FROM users
        LEFT JOIN issued_books
        ON users.id = issued_books.user_id
        ORDER BY users.id, issued_books.issue_date DESC
    """)

    users = cur.fetchall()
    db.close()

    return render_template("profile.html", users=users)


# ============ ADD USER ============
@users_bp.route("/add", methods=["POST"])
def add_user():
    username = request.form.get("username")
    roll_no = request.form.get("roll_no")
    department = request.form.get("department")

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO users (username, roll_no, department, library_id)
        VALUES (?, ?, ?, ?)
    """, (username, roll_no, department, LIBRARY_ID))

    db.commit()
    db.close()

    flash("✅ User saved successfully", "success")
    return redirect(url_for("users.profile"))


# ============ ISSUE BOOK ============
@users_bp.route("/issue-book/<int:user_id>", methods=["POST"])
def issue_book(user_id):
    book_name = request.form.get("book_name", "").strip()

    if not book_name:
        flash("❌ Please enter a book name", "danger")
        return redirect(url_for("users.profile"))

    db = get_db()
    cur = db.cursor()

    # check user
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if not user:
        db.close()
        flash("❌ User not found", "danger")
        return redirect(url_for("users.profile"))

    # check book exists
    cur.execute(
        "SELECT id FROM books WHERE LOWER(book_name) = LOWER(?)",
        (book_name,)
    )
    book = cur.fetchone()

    if not book:
        db.close()
        flash("❌ This book is not present in library", "danger")
        return redirect(url_for("users.profile"))

    # issue book (current date + 10 days return)
    cur.execute("""
        INSERT INTO issued_books (user_id, book_name, issue_date, return_date)
        VALUES (?, ?, DATE('now'), DATE('now', '+10 day'))
    """, (user_id, book_name))

    db.commit()
    db.close()

    flash("✅ Book issued successfully", "success")
    return redirect(url_for("users.profile"))


# ============ DELETE USER ============
@users_bp.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("DELETE FROM issued_books WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))

    db.commit()
    db.close()

    flash("🗑 User deleted successfully", "success")
    return redirect(url_for("users.profile"))