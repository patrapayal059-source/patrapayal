from flask import Blueprint, render_template, request, flash, redirect, url_for
from services.user_service import search_user_by_name, delete_user
from services.issue_service import issue_book_to_user
from database.database import get_db
from datetime import datetime, timedelta

issue_bp = Blueprint("issue", __name__, url_prefix="/issue")

def process_books_with_dates(rows):
    previous_books = []

    for row in rows:
        issue_date_str = row['issue_date']

        # calculate return date (issue + 10 days)
        issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
        expected_return_date = (issue_date + timedelta(days=10)).strftime("%Y-%m-%d")

        previous_books.append({
            "id": row["id"],
            "book_name": row["book_name"],
            "issue_date": issue_date_str,
            "expected_return_date": expected_return_date,
            "actual_return_date": row["return_date"]
        })

    return previous_books




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
                # ✅ GET PREVIOUSLY ISSUED BOOKS (ONLY UNRETURNED ONES)
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                    SELECT id, book_name, issue_date, return_date
                    FROM issued_books
                    WHERE user_id = ? AND return_date IS NULL
                    ORDER BY issue_date DESC
                """, (user['id'],))
                rows = cur.fetchall()
                db.close()
                
                # Process books and add expected return dates
                previous_books = process_books_with_dates(rows)

        # 📕 ISSUE BOOK
        elif "issue" in request.form:
            user_id = request.form.get("user_id")
            book_name = request.form.get("book_name")

            if not user_id or not book_name:
                flash("❌ User or Book is missing!", "danger")
            else:
                result = issue_book_to_user(user_id, book_name)

                if "error" in result:
                    flash(f"❌ {result['error']}", "danger")
                else:
                    issued = result
                    flash("✅ Book issued successfully", "success")
                    
                    # Reload user and previous books
                    db = get_db()
                    cur = db.cursor()
                    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                    user = cur.fetchone()
                    
                    if user:
                        cur.execute("""
                            SELECT id, book_name, issue_date, return_date
                            FROM issued_books
                            WHERE user_id = ? AND return_date IS NULL
                            ORDER BY issue_date DESC
                        """, (user['id'],))
                        rows = cur.fetchall()
                        
                        # Process books and add expected return dates
                        previous_books = process_books_with_dates(rows)
                    
                    db.close()

    # ✅ Handle GET request with username parameter (from profile page)
    elif request.method == "GET":
        username = request.args.get("username")
        if username:
            user = search_user_by_name(username)
            if user:
                # Get previously issued books (only unreturned)
                db = get_db()
                cur = db.cursor()
                cur.execute("""
                    SELECT id, book_name, issue_date, return_date
                    FROM issued_books
                    WHERE user_id = ? AND return_date IS NULL
                    ORDER BY issue_date DESC
                """, (user['id'],))
                rows = cur.fetchall()
                db.close()
                
                # Process books and add expected return dates
                previous_books = process_books_with_dates(rows)

    return render_template("issue_book.html", user=user, issued=issued, previous_books=previous_books)


# ================= ISSUED BOOKS LIST =================
@issue_bp.route("/issued")
def issued_books():
    db = get_db()
    cur = db.cursor()

    # Only show books that haven't been returned yet
    cur.execute("""
        SELECT users.username,
               users.roll_no,
               users.department,
               issued_books.book_name,
               issued_books.issue_date,
               issued_books.return_date,
               issued_books.id as issued_id
        FROM issued_books
        JOIN users ON users.id = issued_books.user_id
        WHERE issued_books.return_date IS NULL
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