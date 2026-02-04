# issue_controller.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.user_service import search_user_by_name, delete_user
from services.issue_service import issue_book_to_user
from database.database import get_db
from datetime import datetime, timedelta

issue_bp = Blueprint("issue", __name__, url_prefix="/issue")


# ================= HELPER =================
def process_books_with_dates(rows):
    books = []

    for row in rows:
        issue_date = datetime.strptime(row["issue_date"], "%Y-%m-%d")
        expected_return_date = (issue_date + timedelta(days=10)).strftime("%Y-%m-%d")

        books.append({
            "id": row["id"],
            "book_name": row["book_name"],
            "issue_date": row["issue_date"],
            "expected_return_date": expected_return_date,
            "actual_return_date": row["return_date"]
        })

    return books


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
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                    SELECT id, book_name, issue_date, return_date
                    FROM issued_books
                    WHERE user_id = ?
                    ORDER BY issue_date DESC
                """, (user["id"],))
                previous_books = process_books_with_dates(cur.fetchall())
                db.close()

        # 📕 ISSUE BOOK
        elif "issue" in request.form:
            user_id = request.form.get("user_id")
            book_name = request.form.get("book_name")

            if not user_id or not book_name:
                flash("❌ User or Book is missing!", "danger")
            else:
                result = issue_book_to_user(user_id, book_name)

                if "error" in result:
                    flash(result["error"], "danger")
                else:
                    flash("✅ Book issued successfully", "success")

                db = get_db()
                cur = db.cursor()
                cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                user = cur.fetchone()

                if user:
                    cur.execute("""
                        SELECT id, book_name, issue_date, return_date
                        FROM issued_books
                        WHERE user_id = ?
                        ORDER BY issue_date DESC
                    """, (user["id"],))
                    previous_books = process_books_with_dates(cur.fetchall())

                db.close()

    return render_template(
        "issue_book.html",
        user=user,
        issued=issued,
        previous_books=previous_books
    )


# ================= ISSUED BOOKS LIST (FIXED) =================
@issue_bp.route("/issued/<int:user_id>")
def issued_books(user_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, book_name, issue_date, return_date
        FROM issued_books
        WHERE user_id = ?
        ORDER BY issue_date DESC
    """, (user_id,))

    issued_list = process_books_with_dates(cur.fetchall())
    db.close()

    return render_template("issued_books.html", issued_list=issued_list)


# ================= DELETE USER =================
@issue_bp.route("/delete/<int:user_id>")
def delete_user_route(user_id):
    delete_user(user_id)
    flash("🗑 User deleted successfully", "success")
    return redirect(url_for("issue.issue_page"))
