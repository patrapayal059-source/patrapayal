from flask import Blueprint, render_template, request, redirect, url_for

users_bp = Blueprint("users", __name__)

# Temporary in-memory storage
USERS = []

@users_bp.route("/users/", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form.get("name")
        rollno = request.form.get("rollno")
        department = request.form.get("department")
        library_id = request.form.get("library_id")

        if name and rollno and department and library_id:
            user = {
                "name": name,
                "rollno": rollno,
                "department": department,
                "library_id": library_id
            }
            USERS.append(user)

        return redirect(url_for("users.profile"))

    return render_template("profile.html", users=USERS)
