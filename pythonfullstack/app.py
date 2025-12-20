import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, redirect, session, render_template
from controllers.auth_controller import auth_blueprint

app = Flask(__name__)
app.secret_key = "library-secret-key"

# -----------------------------
# TEST ROUTE (MUST WORK)
# -----------------------------
@app.route("/test")
def test():
    return "FLASK IS WORKING"

# -----------------------------
# Home route
# -----------------------------
@app.route("/")
def home():
    return "HOME PAGE WORKING"

# -----------------------------
# Register blueprint
# -----------------------------
app.register_blueprint(auth_blueprint)

# -----------------------------
# Run Flask app
# -----------------------------
if __name__ == "__main__":
    print("🚀 Flask running on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
