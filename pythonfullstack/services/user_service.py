from database.db import get_db
from werkzeug.security import check_password_hash

class UserService:

    @staticmethod
    def authenticate(userid, password):
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE userid = ?",
            (userid,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            return user

        return None

