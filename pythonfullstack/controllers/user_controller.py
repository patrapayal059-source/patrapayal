from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.database import get_db

users_bp = Blueprint("users", __name__, url_prefix="/users")

# ================= PROFILE =================
@users_bp.route("/", methods=["GET"])
def profile():
    db = get_db()
    cur = db.cursor()

    # One row per user, latest issued book only
    cur.execute("""
        SELECT 
            u.id,
            u.username,
            u.roll_no,
            u.department,
            ib.book_name,
            ib.issue_date,
            ib.return_date
        FROM users u
        LEFT JOIN issued_books ib
            ON ib.id = (
                SELECT id FROM issued_books
                WHERE user_id = u.id
                ORDER BY issue_date DESC
                LIMIT 1
            )
        ORDER BY u.id
    """)

    users = cur.fetchall()
    db.close()

    return render_template("profile.html", users=users)
# ================= ADD USER =================
@users_bp.route("/add", methods=["POST"])
def add_user():
    username = request.form.get("username")
    roll_no = request.form.get("roll_no")
    department = request.form.get("department")

    LIBRARY_ID = "LIB-2026"   # ✅ common for all users

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO users (username, roll_no, department, library_id)
        VALUES (?, ?, ?, ?)
    """, (username, roll_no, department, LIBRARY_ID))

    db.commit()
    db.close()

    flash("✅ User added successfully", "success")
    return redirect(url_for("users.profile"))


# ================= DELETE USER =================
@users_bp.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db = get_db()
    cur = db.cursor()

    # Delete issued books first (FK safety)
    cur.execute("DELETE FROM issued_books WHERE user_id = ?", (user_id,))
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))

    db.commit()
    db.close()

    flash("🗑 User deleted successfully", "success")
    return redirect(url_for("users.profile"))

# ================= ISSUE BOOK =================
@users_bp.route("/issue/<int:user_id>", methods=["POST"])
def issue_book(user_id):
    book_name = request.form.get("book_name", "Sample Book")

    db = get_db()
    cur = db.cursor()

    # Prevent issuing if user already has a book not returned
    cur.execute("""
        SELECT id FROM issued_books
        WHERE user_id = ? AND return_date IS NULL
    """, (user_id,))

    active_issue = cur.fetchone()

    if active_issue:
        flash("❌ User already has an issued book", "error")
    else:
        cur.execute("""
            INSERT INTO issued_books (user_id, book_name, issue_date)
            VALUES (?, ?, DATE('now'))
        """, (user_id, book_name))

        db.commit()
        flash("✅ Book issued successfully", "success")

    db.close()
    return redirect(url_for("users.profile"))


# ================= RETURN BOOK =================
@users_bp.route("/return/<int:user_id>", methods=["POST"])
def return_book(user_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE issued_books
        SET return_date = DATE('now')
        WHERE user_id = ?
        AND return_date IS NULL
    """, (user_id,))

    db.commit()
    db.close()

    flash("📘 Book returned successfully", "success")
    return redirect(url_for("users.profile"))
