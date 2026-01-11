from database.database import get_connection


def get_users():
    conn = get_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return users


def add_user(name, roll, department, library_id):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (name, roll, department, library_id) VALUES (?, ?, ?, ?)",
        (name, roll, department, library_id)
    )
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
