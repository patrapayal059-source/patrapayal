import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from router import register_routes
from controllers.auth_controller import auth_blueprint

app = Flask(__name__)
app.secret_key = "library-secret-key"

# Register routes & blueprints
register_routes(app)
app.register_blueprint(auth_blueprint)

# ✅ ONLY test route here
@app.route("/test")
def test():
    return "Flask is working!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
