import sqlite3

DB = "pythonfullstack/database/library.db"
from database.database import get_db
def search_user_by_name(username):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT * FROM users WHERE LOWER(username) = LOWER(?)",
        (username,)
    )
    user = cur.fetchone()
    db.close()
    return user


def delete_user(user_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    db.close()

def add_user(username, rollno, department):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (username, rollno, department, library_id)
        VALUES (?, ?, ?, ?)
        """,
        (username, rollno, department, "LIB-2026")
    )

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, username, rollno, department, library_id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cur.fetchone()
    conn.close()
    return user


def delete_user(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))

    conn.commit()
    conn.close()



