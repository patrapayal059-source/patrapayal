from flask import Blueprint, render_template, request
from database.database import get_db

report_bp = Blueprint("report", __name__, url_prefix="/report")

@report_bp.route("/", methods=["GET"])
def report():
    search_date = request.args.get("date")
    search_user = request.args.get("username")

    total_issued = 0
    issued_books = []

    db = get_db()
    cur = db.cursor()

    # fetch all users for dropdown
    cur.execute("SELECT username FROM users")
    users = cur.fetchall()

    if search_date or search_user:
        query = """
            SELECT users.username,
                   issued_books.book_name,
                   issued_books.issue_date,
                   issued_books.return_date
            FROM issued_books
            JOIN users ON users.id = issued_books.user_id
            WHERE 1=1
        """
        params = []

        if search_date:
            query += " AND issued_books.issue_date = ?"
            params.append(search_date)

        if search_user:
            query += " AND users.username = ?"
            params.append(search_user)

        cur.execute(query, params)
        issued_books = cur.fetchall()
        total_issued = len(issued_books)

    db.close()

    return render_template(
        "report.html",
        issued_books=issued_books,
        total_issued=total_issued,
        search_date=search_date,
        users=users,
        search_user=search_user
    )
