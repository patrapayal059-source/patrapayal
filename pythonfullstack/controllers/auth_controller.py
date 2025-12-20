# from flask import Blueprint, request, session, redirect, render_template
# from services.user_service import UserService

# auth_blueprint = Blueprint("auth", __name__)

# @auth_blueprint.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         userid = request.form.get("userid")
#         password = request.form.get("password")

#         user = UserService.authenticate(userid, password)

#         if user:
#             session["user_id"] = user["userid"]
#             return redirect("/")   # go to home page

#         return "Invalid UserID or Password"

#     # GET request
#     return render_template("login.html")
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_blueprint = Blueprint('auth', __name__)

# Dummy user for demonstration
USER = {
    "username": "admin",
    "password": "admin123"
}

# Show login page
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check credentials
        if username == USER['username'] and password == USER['password']:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home page
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


# Logout route
@auth_blueprint.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
