from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.user_service import search_user_by_name, delete_user
from services.issue_service import issue_book_to_user
from database.database import get_db

issue_bp = Blueprint("issue", __name__, url_prefix="/issue")


# ================= ISSUE BOOK PAGE =================
@issue_bp.route("/", methods=["GET", "POST"])
def issue_page():
    user = None
    issued = None
    previous_books = []

    if request.method == "POST":

        # 🔍 SEARCH USER
        if "search" in request.form:
            username = request.form.get("username")
            user = search_user_by_name(username)

            if not user:
                flash("❌ User not found", "danger")
            else:
                # ✅ GET PREVIOUSLY ISSUED BOOKS
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                    SELECT book_name, issue_date, return_date
                    FROM issued_books
                    WHERE user_id = ?
                    ORDER BY issue_date DESC
                """, (user['id'],))
                previous_books = cur.fetchall()
                db.close()

        # 📕 ISSUE BOOK
        elif "issue" in request.form:
            user_id = request.form.get("user_id")
            book_name = request.form.get("book_name")

            result = issue_book_to_user(user_id, book_name)

            if "error" in result:
                flash("❌ This book is not present in library", "danger")
            else:
                issued = result
                flash("✅ Book issued successfully", "success")

    # ✅ Handle GET request with username parameter (from profile page)
    elif request.method == "GET":
        username = request.args.get("username")
        if username:
            user = search_user_by_name(username)
            if user:
                # Get previously issued books
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                    SELECT book_name, issue_date, return_date
                    FROM issued_books
                    WHERE user_id = ?
                    ORDER BY issue_date DESC
                """, (user['id'],))
                previous_books = cur.fetchall()
                db.close()

    return render_template("issue_book.html", user=user, issued=issued, previous_books=previous_books)


# ================= ISSUED BOOKS LIST =================
@issue_bp.route("/issued")
def issued_books():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT users.username,
               issued_books.book_name,
               issued_books.issue_date,
               issued_books.return_date
        FROM issued_books
        JOIN users ON users.id = issued_books.user_id
        ORDER BY issued_books.issue_date DESC
    """)

    issued_list = cur.fetchall()
    db.close()

    return render_template("issued_books.html", issued_list=issued_list)


# ================= DELETE USER =================
@issue_bp.route("/delete/<int:user_id>")
def delete_user_route(user_id):
    delete_user(user_id)
    flash("🗑 User deleted successfully", "success")
    return redirect(url_for("issue.issue_page"))