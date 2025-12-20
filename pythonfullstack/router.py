from flask import send_from_directory
from controllers.books_controller import books_blueprint
import os

FRONTEND_PATH = os.path.join(
    os.path.dirname(__file__),
    "frontend",
    "pages"
)

def register_routes(app):
    app.register_blueprint(books_blueprint, url_prefix="/api/books")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        requested = os.path.join(FRONTEND_PATH, path)
        if path and os.path.exists(requested):
            return send_from_directory(FRONTEND_PATH, path)
        return send_from_directory(FRONTEND_PATH, "index.html")
