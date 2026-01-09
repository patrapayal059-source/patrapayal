from flask import render_template
from controllers.books_controller import books_bp
from controllers.user_controller import user_bp

def register_routes(app):
    app.register_blueprint(books_bp)
    app.register_blueprint(user_bp)

    @app.route("/")
    def index():
        return render_template("index.html")


