
# APP+ROUTET
from flask import Flask, render_template
from controllers.books_controller import books_bp
from controllers.user_controller import users_bp

app = Flask(__name__)  # ✅ DEFAULT is CORRECT

app.register_blueprint(books_bp)
app.register_blueprint(users_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
