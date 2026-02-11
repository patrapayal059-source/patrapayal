# user_controller.py 
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
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
        VALUES ( ?, ?, ?, ?)
    """, (username, roll_no, department, LIBRARY_ID))

    db.commit()
    db.close()

    flash("✅ User added successfully", "success")
    return redirect(url_for("users.profile"))


# ================= EDIT USER - FIXED ROUTE =================
@users_bp.route("/edit/<int:user_id>", methods=["POST"])
def edit_user(user_id):
    """
    Updates user information via AJAX request
    Receives JSON data with username, roll_no, and department
    
    Route: POST /users/edit/<user_id>
    Content-Type: application/json
    """
    print(f"Edit route called for user_id: {user_id}")  # Debug log
    
    try:
        # Get JSON data from request
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log
        
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400
        
        username = data.get("username")
        roll_no = data.get("roll_no")
        department = data.get("department")

        # Validate input
        if not username or not roll_no or not department:
            return jsonify({"success": False, "error": "All fields are required"}), 400

        db = get_db()
        cur = db.cursor()

        # Check if user exists
        cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cur.fetchone():
            db.close()
            return jsonify({"success": False, "error": "User not found"}), 404

        # Update user in database
        cur.execute("""
            UPDATE users
            SET username = ?, roll_no = ?, department = ?
            WHERE id = ?
        """, (username, roll_no, department, user_id))

        db.commit()
        db.close()

        print(f"User {user_id} updated successfully")  # Debug log

        return jsonify({
            "success": True,
            "message": "User updated successfully"
        }), 200

    except Exception as e:
        print(f"Error in edit_user: {str(e)}")  # Debug log
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


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
        # Insert issued book with return date 10 days later
        cur.execute("""
            INSERT INTO issued_books (user_id, book_name, issue_date, return_date)
            VALUES (?, ?, DATE('now'), DATE('now', '+10 day'))
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


# ================= DEBUG ROUTE =================
@users_bp.route("/debug")
def debug():
    """Debug route to test if blueprint is registered"""
    return jsonify({
        "message": "Users blueprint is working!",
        "routes": [
            "/users/",
            "/users/add",
            "/users/edit/<user_id>",
            "/users/delete/<user_id>",
            "/users/issue/<user_id>",
            "/users/return/<user_id>"
        ]
    })