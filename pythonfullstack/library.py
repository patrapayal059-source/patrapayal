
# pythonfullstack/library.py

import sys
import os

# Add the current directory to Python path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template

# import blueprints
from controllers.books_controller import books_bp
from controllers.user_controller import users_bp
from controllers.report_controller import report_bp
from controllers.issue_controller import issue_bp

# ================== CREATE APP FIRST ==================
app = Flask(__name__)

# ================== CONFIG ==================
app.secret_key = "super-secret-key"   # required for flash messages

# ================= REGISTER BLUEPRINTS =================
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)
app.register_blueprint(report_bp)
app.register_blueprint(issue_bp)

# ================== HOME ROUTE ==================
@app.route("/")
def home():
    return render_template("home.html")

# ================== RUN APP ==================
if __name__ == "__main__":
   app.run(debug=True, port=5001)