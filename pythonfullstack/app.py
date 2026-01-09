from flask import Flask
from router import register_routes

app = Flask(__name__)
app.secret_key = "secret123"

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
