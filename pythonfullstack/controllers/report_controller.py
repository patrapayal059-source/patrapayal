from flask import Blueprint, render_template, request
from database.database import get_db
from datetime import datetime, timedelta

report_bp = Blueprint("report", __name__, url_prefix="/report")

@report_bp.route("/", methods=["GET"])
def report():
    search_date = request.args.get("date")
    search_user = request.args.get("username")

    issued_books = []
    total_issued = 0

    db = get_db()
    cur = db.cursor()

    # Users for dropdown
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
        rows = cur.fetchall()

        for row in rows:
            issue_date = datetime.strptime(row["issue_date"], "%Y-%m-%d")
            expected_return_date = (issue_date + timedelta(days=10)).strftime("%Y-%m-%d")

            issued_books.append({
                "username": row["username"],
                "book_name": row["book_name"],
                "issue_date": row["issue_date"],
                "expected_return_date": expected_return_date,
                "actual_return_date": row["return_date"]
            })

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
